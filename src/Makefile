.PHONY: all
all: split

split:
	gcc -Wall ./deps/split.c ./deps/merge.c -o split -lm -pthread

.PHONY: clean
clean:
	rm -rf ./split
	