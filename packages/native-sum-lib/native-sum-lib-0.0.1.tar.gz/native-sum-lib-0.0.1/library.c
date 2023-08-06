int sum(int n, int numbers[]){
    int result = 0;
    for(int i = 0; i < n; i++){
        result += numbers[i];
    }
    return result;
}