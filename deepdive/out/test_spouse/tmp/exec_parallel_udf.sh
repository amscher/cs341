find out/test_spouse/tmp -name 'has_spouse_features.copy_query_func_ext_has_spouse_features.tsv-*' 2>/dev/null -print0 | xargs -0 -P 1 -L 1 bash -c '/Users/jackywang/Desktop/341/project/deepdive/target/scala-2.10/test-classes/spouse/udf/ext_has_spouse_features.py < "$0" > "$0.out"'