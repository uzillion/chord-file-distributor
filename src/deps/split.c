#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <sys/stat.h>
#include "split.h"
#include "merge.h"

#define SIZE 1024

static size_t buffer_size = SIZE;

typedef struct segment_thread {
  unsigned id;
  pthread_t thrd;
  char file_name[100];
  long start_index;
  long end_index;
}SThread;

/**
   * C++ version 0.4 char* style "itoa":
   * Written by Lukás Chmela
   * Released under GPLv3.
*/
static char* itoa(int value, char* result, int base) {
  // check that the base if valid
  if (base < 2 || base > 36) { *result = '\0'; return result; }

  char* ptr = result, *ptr1 = result, tmp_char;
  int tmp_value;

  do {
    tmp_value = value;
    value /= base;
    *ptr++ = "zyxwvutsrqponmlkjihgfedcba9876543210123456789abcdefghijklmnopqrstuvwxyz" [35 + (tmp_value - value * base)];
  } while ( value );

  // Apply negative sign
  if (tmp_value < 0) *ptr++ = '-';
  *ptr-- = '\0';
  while(ptr1 < ptr) {
    tmp_char = *ptr;
    *ptr--= *ptr1;
    *ptr1++ = tmp_char;
  }
  return result;
}

static long get_file_size(char *file_name) {
  FILE *file = fopen(file_name, "r");
  long size = 0L;

  fseek(file, 0L, SEEK_SET);
  fseek(file, 0L, SEEK_END);
  size = ftell(file);
  // printf("\nFile size: %ld bytes\n", size);
  fseek(file, 0L, SEEK_SET);
  fclose(file);

  return size;
}

void * create_segment(void *arg) {
  SThread *segment_data = (SThread *)arg;
  size_t bytes;
  long total = segment_data->start_index;
  char buffer[buffer_size % 2048]; // Max buffer size set to 2KB.
  char output[100], postfix[8];
  FILE *file = fopen(segment_data->file_name, "r");

  if(mkdir("./cache", 0700)) {
  }
  strcpy(output, "./cache/");
  strcat(output, segment_data->file_name);

  // Converting segment id to String
  itoa(segment_data->id, postfix, 10);

  // sprintf(output, "%s_%s", segment_data->file_name, postfix);
  
  // Prepending a '_' character before the postfix segment number
  char temp = postfix[0];
  postfix[0] = '_';
  postfix[1] = temp;
  postfix[2] = '\0';

  // Generating final the segnment name and creating a file to write inside to
  strcat(output, postfix);
  FILE *segment = fopen(output, "w");

  // Setting the start of segment data, and writing it to the segment file.
  fseek(file, segment_data->start_index, SEEK_SET);
  printf("Writing segment %d: %ld to %ld\n", segment_data->id, segment_data->start_index, segment_data->end_index);
  while((bytes = fread(buffer, 1, buffer_size, file))) {
    total = total + bytes;
    // fwrite(buffer, 1, bytes, segment);
    if(total >= (segment_data->end_index)) {
      fwrite(buffer, 1, bytes - (total - segment_data->end_index), segment);
      fflush(segment);
      if(segment_data->end_index == get_file_size(segment_data->file_name)) {
        char td_file_name[100];
        strcpy(td_file_name, segment_data->file_name);
        strcat(td_file_name, ".td");
        FILE *td_file = fopen(td_file_name, "w");
        fprintf(td_file, "%s\n", segment_data->file_name);
        fprintf(td_file, "%d\n", segment_data->id + 1);
        fprintf(td_file, "%ld\n", segment_data->end_index);
        fclose(td_file);
      }
      break;
    }
    fwrite(buffer, 1, bytes, segment);
    fflush(segment);
    
  }

  fclose(file);
  fclose(segment);
  pthread_exit(NULL);
}

/**
 * Splits files into smaller segment
 * 
 * @params: 
 *    input - Input file name
 *    pieces - Number of pieces you want the split the file into
 *    buf_size - Custom buffer size to copy file data to segments; use 0 for default.
 *   
*/
void split(char *input, unsigned pieces, size_t buf_size) {
  long size = 0L, segment_size = 0L;
  SThread segment[pieces];

  if(buf_size > 0)
    buffer_size = buf_size;

  // Getting size of file to be split.  
  size = get_file_size(input);
  
  // Getting average number of bytes per segment.
  segment_size = (long)floor(size/pieces);

  // Assigning thread for each segment
  for(int i = 0; i < pieces; i++) {
    segment[i].id = i;
    strcpy(segment[i].file_name, input);
    segment[i].start_index = (long)(i)*segment_size; 
    if(i < pieces-1)
      segment[i].end_index = (long)(i+1)*segment_size;
    else
      segment[i].end_index = size;
  
    if(pthread_create(&segment[i].thrd, NULL, create_segment, (void *)(segment+i))) {
      fprintf(stderr, "%s %d\n", "Error creating thread", i);
    }

  }

  for(int i = 0; i < pieces; i++) {
    pthread_join(segment[i].thrd, NULL);
  }
  return;
}

int main(int args, char **argv) {
  if(args < 3) {
    fprintf(stderr, "%s\n", "USAGE:");
    fprintf(stderr, "%s\n\n", "For splitting\n\tsplit <file> <pieces> [buffer_size]");
    fprintf(stderr, "%s\n", "For merging\n\tsplit -m <td file>");
  }
  else if(strcmp(argv[1], "-m") == 0) {
    merge(argv[2]);
  }
  else if(args == 3)
    split(argv[1], atoi(argv[2]), 0);
  else
    split(argv[1], atoi(argv[2]), atoi(argv[3]));

  return 0;
}
