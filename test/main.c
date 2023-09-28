#include <stdio.h>
#include <stdlib.h>

// Disable CRT secure warning
#pragma warning(disable:4996)

// Single line comment

/*

Block comment!

*/

#define DLL_EXPORT __declspec(dllexport)


// Simple function. Takes no arguments, returns nothing
DLL_EXPORT
void simple_function(void){
    printf("Simple function. Takes no arguments, returns nothing");
}

/*
  Simple function. Takes no arguments, returns an int (72)
*/
DLL_EXPORT
int function_with_return_value(void){
    printf("Simple function. Takes no arguments, returns an int");
    return 72;
}

DLL_EXPORT
int* function_with_return_allocated_ptr(void){
    printf("Simple function. Takes no arguments, returns a ptr to allocated int");
    int* a = (int*)malloc(sizeof(int));
    *a = 99;
    return a;
}

DLL_EXPORT
float function_with_args(int num){
    printf("Function which takes an int, returns float (arg divided by 2), %i", num);

    return (float)(num/2);
}

DLL_EXPORT
void function_which_modifies_ptr_arg(int* num){
    printf("Function which takes a char* and num, returns string constructed from that");

    *num = 99;
}

DLL_EXPORT
char* function_with_multiple_args(char* s, int num){
    printf("Function which takes a char* and num, returns string constructed from that");

    int str_size = 64;
    char* val = (char*)malloc(str_size*sizeof(char));
    sprintf(val, "Result: %s, %i", s, num);

    return val;
}

struct MyTestStruct {
    int a;
    float b;
};

DLL_EXPORT
struct MyTestStruct function_takes_and_returns_custom_struct(struct MyTestStruct my_struct){
    printf("Function which takes a custom struct, returns the same struct with values multiplied by two");

    my_struct.a *= 2;
    my_struct.b *= 2;

    return my_struct;
}