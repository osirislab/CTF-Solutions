int main ( int	argc, 	char** argv)			
{	
     int	i;	 	   
	
     char	buf[20];	 	  	
	
     for(i=0;i<20;i++)			 	  
	{
     		buf[i] = i;	 	
	
     		if(i%4)	buf[i] += 61;		
	}
     			    
	
     for(i=0;i<20;i+=2)		    	
	{
     		buf[i] ^= buf[(i*3)%20] -1;		
	
     		buf[i+1] ^= 0x40;	 	
	
     	 	if(i % 7)  
	
     			buf[i] += 3;	 
	}
     		 				
	
     for(i=18;i>0;i--)		  			
	{
     		buf[i]	^= 0x81; 	 
	
     		buf[i+1] ^= buf[i] | 0x12;	
	
     		if(buf[i]<0x80) 		 	
	
     		 	buf[i]+=3;	 	
	else
     		 	buf[i] -= 3;	
	
     		buf[(i*3)%2] ^=0x99;			 
	
     		buf[(i*3)%5] ^= 0x33;			
	}
     	  	  	
	
     for(i=0;i<20;i++)			  		
	{
     	buf[i] &= 0x7f;	   
	
     		if(buf[i]<32) buf[i] += 32; 	
	}
     buf[19]=0;			  	 
	
     printf("%s",buf);		  	  
	
return 0; 
}

