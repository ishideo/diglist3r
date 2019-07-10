cat x.txt| jq -r '["\(.domain)", "\(.results|@csv|gsub("\"";""))"]|@tsv'> x.tsv
