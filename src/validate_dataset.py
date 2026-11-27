"""Kiểm tra nhanh tệp huấn luyện WiDS của đồ án."""

import argparse
from pathlib import Path
import sys

if __package__:
    from .tabular_data import load_data, numerical_columns
else:
    from tabular_data import load_data, numerical_columns

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / 'data/raw/training.csv'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', type=Path, default=DEFAULT_CSV, help='Đường dẫn tệp training.csv')
    args = parser.parse_args()
    try:
        frame, checksum = load_data(ROOT, csv_path=args.csv)
    except (OSError, ValueError) as error:
        print(f'Không thể sử dụng tệp huấn luyện WiDS: {error}', file=sys.stderr)
        return 1

    n_numeric = len(numerical_columns(frame))
    print(f'{args.csv}: {len(frame):,} dòng × {len(frame.columns)} cột')
    print(f'{n_numeric} biến số và {len(frame.columns) - n_numeric - 2} trường phân loại, mã hoặc mô tả')
    print(f'SHA-256: {checksum}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
