.data
	inputStr: .space 8		#space in memory for user input
	str2Int: .space 8		#space in memory for converted integer
	prompt: .asciiz "Enter a two-digit integer [00-99]: "
	binarySentence: .asciiz "The binary representation of your integer is: "
	nextLine: .asciiz "\n"
	asciiDiff: .word 48
	
.text
	#display prompt
	li $v0, 4
	la $a0, prompt
	syscall
	
	#get user input as a string
	li $v0, 8
	la $a0, inputStr
	li $a1, 8
	syscall			# inputStr Ready
	
	#convert to integer
	#store input in memory
	li $s0, 0x10010000
	
	#load first ascii character
	lb $t1, 0x00($s0)
	
	#load second
	lb $t2, 0x01($s0)
	
	#store first
	li $s1, 0x10010040
	sb $t1, 0($s1)
	
	#store second
	li $s2, 0x10010044
	sb $t2, 0($s2)
	
	#convert to int, digits are seperate
	lw $s7, asciiDiff
	sub $t3, $t1, $s7
	sub $t4, $t2, $s7
	
	#put digits together by multiplying first digit by 10 and adding second digit
	mul $s3, $t3, 10
	add $s3, $s3, $t4
	
	
	sw $s3, str2Int			#  str2Int Ready
	
	#convert to binary
	