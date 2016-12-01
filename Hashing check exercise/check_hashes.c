/* Copyright (C) 2009 Trend Micro Inc.
 * All right reserved.
 *
 * This program is a free software; you can redistribute it
 * and/or modify it under the terms of the GNU General Public
 * License (version 2) as published by the FSF - Free Software
 * Foundation
 */


/* 
 * @autor José Arcos Aneas
 * @date 13 Mar 2016
 *
 * Using the library md5_op.h OSSEC this 
 * simple program checks the md5 value 
 * assigned to an ID matches its real value.
 * 
 * $: cc -W -Wall -c md5.c md5_op.c 
 * $: ar cru md5_op.a md5_op.o md5.o
 * $: ranlib md5_op.a
 * $: cc -o check_hashes check_hashes.c md5_op.a
 * $: ./check_hashes data.txt 
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "md5_op.h"
/*
 * Function to display using the program  
 *
*/
void usage(char **argv)
{
    printf("Use:\t%s data.txt\n", argv[0]);
    return;
}
/*
 * Main function for verifying whether the 
 * md5 value assigned to the file is correct.
 */
int main(int argc, char **argv)
{
	os_md5 filesum; 
    // initial checks 

    if (argc != 2) {
        usage(argv);
    }
    // Read the file and verify that it has been read
    FILE *fp;
    fp = fopen(argv[1], "rb");
    if (!fp) {
    	return (0);
    }
    // Process each line of the file individually
	char cadena[100];
	while (fgets(cadena, 100, fp) != NULL)
	{
		// Declaration of local variables
		char **linea;
		char *id = strtok( cadena, " ");
      	char *name = strtok( NULL, " ");
		char *md5 = strtok(NULL, " ");
        char *p, *q, *h, *res; 
   		int num_chars; 
		//printf( "%s %s %s", id , name, md5);
		// Calculate the number of characters in the strings 
	    for (num_chars = 0, p = id; *p != '\0'; num_chars++, p++) ; 
	    for (p = name; *p != '\0'; num_chars++, p++); 
		// reserve space
	    res = (char *) malloc(num_chars); 
		// copy string 
	    for (p =res, q = id; (*p = *q) != '\0'; p++, q++) ; 
	    for (q = name; (*p = *q) != '\0'; p++, q++) ; 
        // calculate the real value of md5 and store it in the variable filesum
        OS_MD5_Str(res, filesum);        
         
        //printf("Filesum : %s\n",filesum);
        //printf("md5     : %s",md5);

    
        if( strncmp(md5,filesum,32) == 0) printf("%s OK\n",id);
        else printf("%s FAIL\n",id);
    }
}




























 
