#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "merge.h"

void merge(char* input) {
  FILE *td_file = fopen(input, "r");
  size_t bytes;
  int count = 0;
  char *line = NULL;
  char name[100];
  int segments = 0;
  size_t length = 0;
  size_t size;
  while ((bytes = getline(&line, &length, td_file)) != -1) {
    switch (count)
    {
      case 0:
        strcpy(name, line);
        int temp = strlen(name);
        name[temp-1] = '\0'; 
        break;
      case 1:
        segments = atoi(line);
        break;
      case 2:
        size = atoi(line);
        break;
      default:
        break;
    }
    count++;
  }
  printf("%s\n", name);
  // Should be improved using threads
  char merged_name[100];
  // merged_name[0] = 'h';
  // merged_name[1] = 'o';
  // printf("hello: %s\n", merged_name);
  strcpy(merged_name, "./cache/");
  // printf("filed merged:  %s", merged_name);
  strcat(merged_name, name);
  // printf("filed merged:  %s", merged_name);
  FILE *merged_file = fopen(merged_name, "w");
  // printf("filed merged:  %d", merged_file->_fileno);
  for(int i = 0; i < segments; i++) {
    char buff[1024];
    char segment_name[100];
    size_t sbytes;
    sprintf(segment_name, "./cache/%s_%d", name, i);
    FILE *segment = fopen(segment_name, "r");
    int total = 0;
    while((sbytes = fread(buff, 1, 1024, segment))) {
      total += sbytes;
      fwrite(buff, 1, sbytes, merged_file);
      fflush(merged_file);
    }
    printf("%s: %d\n", segment_name, total);
    fclose(segment);
  }
  fclose(merged_file);
  return;
}
