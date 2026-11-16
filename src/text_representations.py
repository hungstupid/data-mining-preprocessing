"""Small, testable representation diagnostics; experiment orchestration stays in Stage 04."""
from itertools import combinations
import zlib

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer, normalize
from sklearn.svm import LinearSVC
from sklearn.metrics import silhouette_score


def fixed_text_folds(labels, base_texts, *, n_splits=5, seed=42):
    """Exactly the Stage 03 recipe: grouping before any representation-specific change."""
    labels = np.asarray(labels)
    groups = pd.factorize(pd.Series(base_texts), sort=True)[0]
    if len(np.unique(groups)) < len(groups):
        splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
        folds = list(splitter.split(np.zeros(len(labels)), labels, groups))
    else:
        splitter = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
        folds = list(splitter.split(np.zeros(len(labels)), labels))
    return folds, groups


def word_vectorizer(*, tfidf=True, max_n=1, max_features=30000, min_df=2):
    """Space-joined lexical tokens; built-in WORD analyzer really constructs n-grams.

    A callable analyzer would bypass ngram_range. str.split retains single letters,
    numbers and apostrophized tokens without applying a second regex or lowercasing.
    """
    constructor = TfidfVectorizer if tfidf else CountVectorizer
    parameters = dict(analyzer="word", tokenizer=str.split, preprocessor=None,
                      token_pattern=None, lowercase=False, ngram_range=(1, max_n),
                      min_df=min_df, max_df=1.0, max_features=max_features, dtype=np.float64)
    if tfidf:
        parameters.update(sublinear_tf=True, use_idf=True, smooth_idf=True, norm="l2")
    return constructor(**parameters)


def linear_svm():
    return LinearSVC(C=1.0, dual=False, loss="squared_hinge", tol=1e-4,
                     max_iter=10000, random_state=42, class_weight=None)


def sparse_svm_pipeline(*, tfidf=True, max_n=1, max_features=30000, min_df=2):
    return Pipeline([
        ("vectorizer", word_vectorizer(tfidf=tfidf, max_n=max_n,
                                       max_features=max_features, min_df=min_df)),
        ("unit_norm", Normalizer(norm="l2")),
        ("classifier", linear_svm()),
    ])


def row_norms(matrix):
    if sparse.issparse(matrix):
        return np.sqrt(np.asarray(matrix.multiply(matrix).sum(axis=1)).ravel())
    return np.linalg.norm(np.asarray(matrix), axis=1)


def matrix_profile(matrix):
    """Stored CSR buffers or dense array bytes; explicit sparse zeros are not nonzeros."""
    rows, columns = matrix.shape
    if sparse.issparse(matrix):
        stored = matrix.tocsr(copy=False)
        nonzeros = int(stored.count_nonzero())
        nbytes = stored.data.nbytes + stored.indices.nbytes + stored.indptr.nbytes
        layout = "CSR"
    else:
        stored = np.asarray(matrix)
        nonzeros = int(np.count_nonzero(stored))
        nbytes = stored.nbytes
        layout = "dense"
    cells = rows * columns
    return dict(documents=rows, dimensions=columns, nnz=nonzeros,
                sparsity=1-nonzeros/cells if cells else np.nan,
                storage_bytes=int(nbytes), dense_equivalent_bytes=int(cells*stored.dtype.itemsize),
                zero_documents=int(np.count_nonzero(row_norms(stored)==0)), layout=layout)


def paired_cosines(matrix, pairs):
    """One dot product per sampled pair after L2 normalization; zero-vector cosine is 0."""
    unit = normalize(matrix, norm="l2", copy=True)
    indices = np.asarray(pairs, dtype=int)
    left, right = unit[indices[:, 0]], unit[indices[:, 1]]
    if sparse.issparse(unit):
        values = np.asarray(left.multiply(right).sum(axis=1)).ravel()
    else:
        values = np.einsum("ij,ij->i", left, right)
    return np.clip(values, -1, 1)


def sample_document_pairs(labels, *, same_per_class=600, different_per_class_pair=400, seed=42):
    """Unique unordered non-self pairs, equal quota per class / unordered class pair."""
    labels = np.asarray(labels)
    classes = np.unique(labels)
    positions = {label: np.flatnonzero(labels == label) for label in classes}
    rng = np.random.default_rng(seed)
    records = []
    for left_class, right_class in [(c,c) for c in classes] + list(combinations(classes,2)):
        same = left_class == right_class
        quota = same_per_class if same else different_per_class_pair
        left, right = positions[left_class], positions[right_class]
        available = len(left)*(len(left)-1)//2 if same else len(left)*len(right)
        if quota > available or quota < 0:
            raise ValueError("Pair quota exceeds distinct available pairs")
        selected = set()
        while len(selected) < quota:
            if same:
                a,b = rng.choice(left, size=2, replace=False)
            else:
                a,b = rng.choice(left), rng.choice(right)
            selected.add(tuple(sorted((int(a),int(b)))))
        for a,b in sorted(selected):
            records.append(dict(i=a,j=b,same_class=same,class_a=left_class,class_b=right_class))
    return pd.DataFrame(records, columns=["i","j","same_class","class_a","class_b"])


def balanced_subset(labels, *, per_class=300, seed=42):
    labels = np.asarray(labels)
    rng = np.random.default_rng(seed)
    selected = []
    for label in np.unique(labels):
        positions = np.flatnonzero(labels == label)
        if per_class > len(positions):
            raise ValueError("Subset quota exceeds class support")
        selected.extend(rng.choice(positions, size=per_class, replace=False).tolist())
    return np.sort(selected)


def stable_word_hash(word):
    return zlib.crc32(word.encode("utf-8"))


def mean_word_vectors(documents, vectors):
    """Occurrence-weighted arithmetic mean of known words; all-OOV/empty stays zero."""
    output = np.zeros((len(documents), vectors.vector_size), dtype=np.float32)
    total = unknown = 0
    for i,tokens in enumerate(documents):
        known = [token for token in tokens if token in vectors]
        total += len(tokens)
        unknown += len(tokens)-len(known)
        if known:
            output[i] = np.mean([vectors[token] for token in known], axis=0)
    return output, dict(token_occurrences=total, OOV_occurrences=unknown,
                        OOV_rate=unknown/total if total else np.nan,
                        zero_documents=int(np.count_nonzero(row_norms(output)==0)))


def frozen_sentence_vectors(model, texts, *, batch_size=32):
    """No fit/adaptation; empty strings explicitly receive zero vectors, with rows kept."""
    output = np.asarray(model.encode(list(texts), batch_size=batch_size,
        normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False), dtype=np.float32)
    empty = np.array([not text.strip() for text in texts])
    output[empty] = 0
    return output


def safe_silhouette(matrix, labels, *, metric="cosine", max_documents=2000):
    labels = np.asarray(labels)
    if matrix.shape[0] != len(labels):
        raise ValueError("Silhouette row/label mismatch")
    if len(labels) > max_documents:
        raise ValueError("Use the declared bounded silhouette subset, not the full corpus")
    unique = len(np.unique(labels))
    if not 2 <= unique < len(labels):
        return np.nan, "invalid_label_count"
    data = matrix.data if sparse.issparse(matrix) else np.asarray(matrix)
    if not np.isfinite(data).all():
        return np.nan, "nonfinite_values"
    if np.any(row_norms(matrix)==0):
        return np.nan, "zero_vectors"
    return float(silhouette_score(matrix, labels, metric=metric)), "ok"


def word2vec_numeric_guard():
    """Public scoring regression for gensim #3665; fail instead of accepting -1→0.

    Two opposite Huffman leaves must have equal joint score when all dot-product signs
    reverse. No training/download is needed. See upstream PR #3668 for the underlying fix.
    """
    from gensim.models import Word2Vec
    largest_error = 0.0
    cases = 0
    for algorithm in [0, 1]:
        for dimensions in [1, 4]:
            model = Word2Vec(vector_size=dimensions, min_count=1, hs=1, negative=0,
                             sg=algorithm, workers=1, window=1, seed=42)
            documents = [["left", "right"]]
            model.build_vocab(documents)
            model.wv.vectors[:] = 0
            model.wv.vectors[:, 0] = 1
            model.syn1[:] = 0
            neutral = model.score(documents, total_sentences=1)
            model.syn1[:, 0] = 1
            positive = model.score(documents, total_sentences=1)
            model.syn1[:, 0] = -1
            negative = model.score(documents, total_sentences=1)
            error = float(np.max(np.abs(positive-negative)))
            largest_error = max(largest_error, error)
            if not np.allclose(positive, negative, atol=1e-6) or not negative[0] < neutral[0]:
                raise RuntimeError("gensim BLAS negative-one regression failed; install the exact corrected source pin in requirements-lock.txt")
            cases += 1
    return dict(passed_cases=cases, max_symmetry_error=largest_error)
