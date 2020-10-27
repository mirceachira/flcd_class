%{
    #include "langCodes.h"
%}

letter              [a-zA-Z]
digit               [0-9]

%%


"begin"                 { return CODE_OF_begin; }
"end"                   { return CODE_OF_end; }

"int"                   { return CODE_OF_int; }
"char"                  { return CODE_OF_char; }

"read"                  { return CODE_OF_read; }
"write"                 { return CODE_OF_write; }

"if"                    { return CODE_OF_if; }
"while"                 { return CODE_OF_while; }
"do"                    { return CODE_OF_do; }
{digit}+                { return CODE_OF_unsigned_int; }

"("                     { return CODE_OF_l_par; }
")"                     { return CODE_OF_r_par; }

">"                     { return CODE_OF_gt; }
">="                    { return CODE_OF_gte; }

"<"                     { return CODE_OF_lt; }
"<="                    { return CODE_OF_lte; }

"="                     { return CODE_OF_eq; }
"!="                    { return CODE_OF_neq; }

";"                     { return CODE_OF_semicolon; }

"%"                     { return CODE_OF_perc; }
"+"                     { return CODE_OF_plus; }

[a-zA-Z_][a-zA-Z0-9_]*  { return CODE_OF_identifier; }

[ \t\n]+                /* eat up whitespace */

%%
#include <stdio.h>
#include <string.h>


int getCodePosition(char *identifier, int size, char arr[100][100]) {
    for (int i=0; i<size; i++) {
        if (strcmp(identifier, arr[i]) == 0) {
            return i;
        }
    }
    return -1;
}


int main(int argc, char** argv)
{
    ++argv, --argc;  /* skip over program name */
    if ( argc > 0 )
            yyin = fopen( argv[0], "r" );
    else
            yyin = stdin;

    FILE * pifFile;
    FILE * stFile;

    pifFile = fopen("generated_pif.txt", "w+");
    fprintf(pifFile, "COD\tPOZ in ST\n");

    stFile = fopen("generated_st.txt", "w+");

    // This should be implemented as a hash table for better scaling!
    char  identifierArr[100][100];
    int size = 0;

    int currentRuleResult = yylex();
    while (currentRuleResult) {  // assuming all rules return integer codes != 0
        if (currentRuleResult == CODE_OF_identifier || currentRuleResult == CODE_OF_unsigned_int) {
            int codePosition = getCodePosition(yytext, size, identifierArr);

            if (codePosition == -1) {   // add new identifier in symbol table
                strcpy(identifierArr[size], yytext);

                fprintf(stFile, "%s\n", yytext);
                fprintf(pifFile, "%d\t%d\n", currentRuleResult, size);
                size += 1;
            } else {
                fprintf(pifFile, "%d\t%d\n", currentRuleResult, size);
            }
        } else { //
            fprintf(pifFile, "%d\t%d\n", currentRuleResult, -1);
        }

        currentRuleResult = yylex();
    }

    fclose(pifFile);
    fclose(stFile);
}

#ifndef yywrap
   int yywrap() { return 1; }
#endif