CC = gcc
testName = test
SRC_DIR = src
LIB_DIR = src/libpnt

test: $(SRC_DIR)/test.c $(wildcard $(LIB_DIR)/*.c)
	$(CC) $(SRC_DIR)/test.c $(wildcard $(LIB_DIR)/*.c) -o $(testName)