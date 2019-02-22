.PHONY: all
all: split

split:
	gcc -Wall split.c merge.c -o split -pthread

.PHONY: clean
clean:
	rm -rf ./split
	