find out/test_chunking/tmp -name 'word_features.copy_query_func_ext_features.tsv-*' 2>/dev/null -print0 | xargs -0 -P 1 -L 1 bash -c '/Users/jackywang/Desktop/341/project/deepdive/target/scala-2.10/test-classes/chunking/udf/ext_features.py < "$0" > "$0.out"'
