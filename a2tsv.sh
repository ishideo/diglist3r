cat a.txt| jq -r '["\(.domain)", "\(.results|@csv|gsub("\"";""))"]|@tsv'> a.tsv
