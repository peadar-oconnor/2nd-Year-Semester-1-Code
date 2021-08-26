.data
	inputStr: .space 20		#space in memory for user input
	prompt: .asciiz "Enter a real number [xxx.yyy]: "
	asciiDiff: .word 48
	str2float: .space 20
	
.text
	#display prompt
	li $v0, 4
	la $a0, prompt
	syscall
	
	#get user input as a string
	li $v0, 8
	la $a0, inputStr
	li $a1, 20
	syscall			# inputStr Ready
	
	#convert to integer equivalents of exponent and fraction
	#store input in memory
	li $s0, 0x10010000
	li $s1, 0x10010004
	
	#load individual ascii characters into t registers
	lb $t1, 0x00($s0)
	lb $t2, 0x01($s0)
	lb $t3, 0x02($s0)
	lb $t4, 0x00($s1)
	lb $t5, 0x01($s1)
	lb $t6, 0x02($s1)
	
	#convert each to int
	lw $t7, asciiDiff
	sub $t1, $t1, $t7
	sub $t2, $t2, $t7
	sub $t3, $t3, $t7
	sub $t4, $t4, $t7
	sub $t5, $t5, $t7
	sub $t6, $t6, $t7
	
	#create what the exponent will be by putting first 3 digits together: multiplying first by 100, second by 10 and adding the three digits
	mul $s1, $t1, 100
	mul $s2, $t2, 10
	add $s1, $s1, $s2
	add $s1, $s1, $t3
	
	#create what the fraction will be by putting second 3 digits together: multiplying first by 100, second by 10 and adding the three digits
	mul $s3, $t4, 100
	mul $s4, $t5, 10
	add $s3, $s3, $s4
	add $s3, $s3, $t6
	
	#move to coprocessor 1
	mtc1 $s1, $f1
	mtc1 $s3, $f2
	
	#convert to float
	cvt.s.w $f1, $f1
	cvt.s.w $f2, $f2
	#divide yyy by 1000 to put it after the decimal point
	addi $t0, $zero, 1000
	mtc1, $t0, $f3
	cvt.s.w $f3, $f3
	div.s $f2, $f2, $f3
	add.s $f0, $f1, $f2
	
	swc1 $f0, str2float		#str2float ready