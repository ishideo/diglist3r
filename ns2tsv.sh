cat ns.txt| jq -r '["\(.domain)", "\(.results|@csv|gsub("\"";""))"]|@tsv' > ns.tsv
