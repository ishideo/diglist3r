cat ns.txt| jq -r '["\(.domain)", "\(.result|@csv|gsub("\"";""))"]|@tsv' > ns.tsv
