"""Small known-answer checks. No transformer download or large model fitting in unit tests."""
import ast
from pathlib import Path
import unittest

import nbformat
import numpy as np
import pandas as pd
from scipy import sparse

from src.text_data import LABELS, make_text_protocol
from src.text_representations import (fixed_text_folds, word_vectorizer, sparse_svm_pipeline,
    matrix_profile, paired_cosines, sample_document_pairs, balanced_subset,
    mean_word_vectors, frozen_sentence_vectors, safe_silhouette, word2vec_numeric_guard)


class RepresentationTests(unittest.TestCase):
    def test_outer_recipe_is_unchanged_and_duplicate_rows_do_not_shift_population(self):
        raw=pd.DataFrame([(label,f"{label} product {i}") for label in LABELS for i in range(5)],
                         columns=["label","text"],dtype="string")
        raw=pd.concat([raw,pd.DataFrame({"label":["Household"],"text":[" HOUSEHOLD  product ０ "]},dtype="string")],ignore_index=True)
        result=make_text_protocol(raw,test_size=.2,seed=42)
        self.assertEqual((len(result['corpus']),len(result['train']),len(result['test'])),(20,16,4))
        self.assertEqual(result['corpus'].row_id.tolist(),list(range(20)))
        self.assertEqual(set(result['test'].label),set(LABELS))
        self.assertTrue(set(result['train'].canonical_key).isdisjoint(result['test'].canonical_key))
        second=make_text_protocol(raw,test_size=.2,seed=42)
        self.assertEqual(result['train'].row_id.tolist(),second['train'].row_id.tolist())

    def test_fixed_group_folds_are_reproducible_and_group_disjoint(self):
        labels=np.array(['A']*6+['B']*6)
        texts=[f'{c}{i}' for c in ['A','B'] for i in range(3) for _ in range(2)]
        first,groups=fixed_text_folds(labels,texts,n_splits=3,seed=42)
        second,_=fixed_text_folds(labels,texts,n_splits=3,seed=42)
        uses=np.zeros(len(labels),dtype=int)
        for (a,b),(c,d) in zip(first,second):
            np.testing.assert_array_equal(a,c);np.testing.assert_array_equal(b,d)
            self.assertTrue(set(groups[a]).isdisjoint(groups[b]));uses[b]+=1
        np.testing.assert_array_equal(uses,np.ones(len(labels)))

    def test_word_analyzer_really_builds_ngrams_with_numbers_and_one_letter(self):
        vectorizer=word_vectorizer(tfidf=False,max_n=3,max_features=None,min_df=1)
        vectorizer.fit(['a 3 b'])
        self.assertEqual(set(vectorizer.get_feature_names_out()),{'a','3','b','a 3','3 b','a 3 b'})

    def test_sparse_and_dense_profiles_count_numerical_nonzeros(self):
        dense=np.array([[1.,0.],[0.,0.]])
        explicit_zero=sparse.csr_matrix((np.array([1.,0.]),np.array([0,1]),np.array([0,2,2])),shape=(2,2))
        for matrix in [dense,explicit_zero]:
            result=matrix_profile(matrix)
            self.assertEqual((result['documents'],result['dimensions'],result['nnz']),(2,2,1))
            self.assertEqual(result['sparsity'],.75);self.assertEqual(result['zero_documents'],1)
        self.assertEqual(matrix_profile(dense)['storage_bytes'],dense.nbytes)
        self.assertEqual(matrix_profile(explicit_zero)['storage_bytes'],
                         explicit_zero.data.nbytes+explicit_zero.indices.nbytes+explicit_zero.indptr.nbytes)

    def test_paired_cosines_sparse_dense_and_zero_convention(self):
        matrix=np.array([[1.,0.],[0.,1.],[1.,1.],[0.,0.],[-1.,0.]])
        pairs=np.array([[0,0],[0,1],[0,2],[0,3],[0,4]])
        expected=np.array([1,0,1/np.sqrt(2),0,-1])
        for values in [matrix,sparse.csr_matrix(matrix)]:
            np.testing.assert_allclose(paired_cosines(values,pairs),expected,atol=1e-12)

    def test_pair_and_subset_sampling_have_fixed_quotas_and_no_self_pairs(self):
        labels=np.repeat(['A','B','C','D'],4)
        first=sample_document_pairs(labels,same_per_class=2,different_per_class_pair=1,seed=42)
        second=sample_document_pairs(labels,same_per_class=2,different_per_class_pair=1,seed=42)
        pd.testing.assert_frame_equal(first,second)
        self.assertEqual((first.same_class.sum(),(~first.same_class).sum()),(8,6))
        self.assertFalse((first.i==first.j).any());self.assertFalse(first[['i','j']].duplicated().any())
        np.testing.assert_array_equal(labels[first.i]==labels[first.j],first.same_class)
        for _,rows in first.groupby(['same_class','class_a','class_b']):
            self.assertEqual(len(rows),2 if rows.same_class.iloc[0] else 1)
        subset=balanced_subset(labels,per_class=2,seed=42)
        np.testing.assert_array_equal(subset,balanced_subset(labels,per_class=2,seed=42))
        self.assertEqual(len(np.unique(subset)),8)
        self.assertTrue(all((labels[subset]==c).sum()==2 for c in np.unique(labels)))
        with self.assertRaises(ValueError):sample_document_pairs(labels,same_per_class=100)

    def test_mean_pooling_oov_and_zero_rows_keep_occurrence_weights(self):
        class TinyVectors:
            vector_size=2
            values={'known':np.array([1.,0.]),'other':np.array([0.,1.])}
            def __contains__(self,key):return key in self.values
            def __getitem__(self,key):return self.values[key]
        vectors,report=mean_word_vectors([['known','known','other','M3'],['M3'],[]],TinyVectors())
        np.testing.assert_allclose(vectors,[[2/3,1/3],[0,0],[0,0]],atol=1e-7)
        self.assertEqual((report['token_occurrences'],report['OOV_occurrences'],report['zero_documents']),(5,2,2))
        self.assertAlmostEqual(report['OOV_rate'],.4)

    def test_frozen_encoding_has_no_fit_and_explicit_empty_handling(self):
        class FrozenFixture:
            def encode(self,texts,**kwargs):
                self.call=(texts,kwargs)
                return np.ones((len(texts),3),dtype=np.float32)
        encoder=FrozenFixture()
        output=frozen_sentence_vectors(encoder,['product 3',''],batch_size=2)
        np.testing.assert_array_equal(output,[[1,1,1],[0,0,0]])
        self.assertEqual(encoder.call[0],['product 3',''])
        self.assertTrue(encoder.call[1]['normalize_embeddings'])

    def test_cv_pipeline_never_learns_validation_vocabulary_or_idf(self):
        texts=['alpha shared','alpha other','beta shared','beta other']
        labels=['A','A','B','B']
        for tfidf in [False,True]:
            model=sparse_svm_pipeline(tfidf=tfidf,max_n=1,min_df=1,max_features=None)
            model.fit(texts,labels)
            model.predict(['validation_only_sentinel shared'])
            vectorizer=model.named_steps['vectorizer']
            self.assertNotIn('validation_only_sentinel',vectorizer.vocabulary_)
            self.assertEqual(set(vectorizer.vocabulary_),{'alpha','beta','shared','other'})
            if tfidf:self.assertAlmostEqual(vectorizer.idf_[vectorizer.vocabulary_['shared']],np.log(5/3)+1)

    def test_valid_and_invalid_silhouettes_are_explicit(self):
        matrix=np.array([[1.,0.],[1.,0.],[0.,1.],[0.,1.]])
        value,status=safe_silhouette(matrix,[0,0,1,1])
        self.assertEqual(status,'ok');self.assertAlmostEqual(value,1)
        for labels in [[0,0,0,0],[0,1,2,3]]:
            value,status=safe_silhouette(matrix,labels)
            self.assertTrue(np.isnan(value));self.assertEqual(status,'invalid_label_count')
        zeros=matrix.copy();zeros[0]=0
        self.assertEqual(safe_silhouette(zeros,[0,0,1,1])[1],'zero_vectors')
        with self.assertRaises(ValueError):safe_silhouette(matrix,[0,0,1,1],max_documents=2)

    def test_word2vec_native_negative_one_guard_without_training_or_download(self):
        report=word2vec_numeric_guard()
        self.assertEqual(report['passed_cases'],4)
        self.assertAlmostEqual(report['max_symmetry_error'],0)

    def test_notebook_schema_imports_and_saved_outputs_have_no_errors(self):
        path=Path(__file__).resolve().parents[1]/'book/text/04_representations.ipynb'
        notebook=nbformat.read(path,as_version=4);nbformat.validate(notebook)
        source='\n'.join(c.source for c in notebook.cells if c.cell_type=='code')
        tree=ast.parse(source)
        imported={node.module for node in ast.walk(tree) if isinstance(node,ast.ImportFrom)}
        self.assertIn('src.text_data',imported);self.assertIn('src.text_preprocessing',imported)
        self.assertIn('src.text_representations',imported)
        self.assertNotIn('nbclient',imported);self.assertNotIn('nbformat',imported)
        self.assertNotIn('read_pickle',source)
        self.assertFalse(any(o.output_type=='error' for c in notebook.cells for o in c.get('outputs',[])))
        self.assertEqual(notebook.metadata.kernelspec.name,'hcmus-wids')


if __name__=='__main__':unittest.main()
