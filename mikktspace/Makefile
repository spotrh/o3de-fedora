CFLAGS := -fPIC -O3 -g -Wall -Werror
CC := gcc
MAJOR := 1
MINOR := 0
NAME := mikktspace
VERSION := $(MAJOR).$(MINOR)

lib: lib$(NAME).so.$(VERSION) 

lib$(NAME).so.$(VERSION): $(NAME).o
	$(CC) -shared -Wl,-soname,lib$(NAME).so.$(MAJOR) $^ -o $@

clean:
	$(RM) *.o *.so*
