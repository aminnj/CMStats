
### Simple scripts to keep track of [CubeMania](https://www.cubemania.org/) times

CM only keeps track of up to 150 individual solves in their database, so they need to be fetched 
every now and then to save them forever.

#### Dependencies

* matplotlib, numpy, pandas (plotting)
* [jq](https://stedolan.github.io/jq/) for command line scripts because the collection script outputs .jsonl

#### Instructions

* Log into CM and visit the TIMER tab. Open dev tools in the browser (cmd+opt+i in Chrome on MacOS) and check the network tab after refreshing the page. Take note of the `user_id` field and paste this into `collect.py`

* Run `python collect.py >> log.txt` manually or in a cron job (note the `>>` and not `>`)

* Quickly check outputs with `./scripts/print_unique.sh log.txt`. This prints out 3 columns of the solve ID, date, time (milliseconds) for unique solves, because `log.txt` will contain duplicates, until I change the collection script to deal with them properly.

* Make plots/fits with `python plot.py -i log.txt` (`-i` is optional and defaults to `log.txt`). Output goes into `plots/`.


