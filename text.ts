function longest_palindrome_string(tests: string): string {
    let maximum_len = 0;
    let start = 0;
   
    const expandAroundCenter = (test: string, left: number, right: number): void => {
    while (left>= 0 && right < test.length && test[left] === test[right]) {
   left--;
    right++;
    }
   
    let  current_length = right - left - 1;
    if  (current_length > maximum_len) {
    maximum_len = current_length;
    start = left + 1;
    }
    };
    for (let i = 0; i < test.length; i++) {
   
    expandAroundCenter(test, i, i);
   
    expandAroundCenter(test, i, i + 1); 
   
    }
   
    let final_result = "";
    for (let i = start; i < start +  maximum_len; i++) {
     final_result += test[i];
    }
    return  final_result ;
   }
   const test = "xyzabcba";
   console.log(longest_palindrome_string(test));
   
   