cat a.txt| jq -r '["\(.domain)", "\(.result|@csv|gsub("\"";""))"]|@tsv'> a.tsv
