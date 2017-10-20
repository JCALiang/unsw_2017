#!/usr/bin/perl -w
# http://www.cse.unsw.edu.au/~cs2041/assignments/pypl
# written by Chieh-An Liang September 2017

$loop_no=0;
my %array;

while ($line = <>) {
	my @temp;
	my @array;
 
    #judge if the line is in any loop-- check current position
	if ($line=~ /^\s{4}\S.*$/){
		$current=1;
	} elsif ($line=~ /^\s{8}\S.*$/){
		$current=2;
	} elsif ($line=~ /^\s{12}\S.*$/){
		$current=3;
	} else {
		$current=0;}
	# check level of indentation
	if ($loop_no > 0 && $current<$loop_no){
		$q=$loop_no-$current;

		foreach $i (0..$q-1){
			print "}\n";
			$loop_no=$loop_no-1;}
	}
		
	chomp $line;

	#remove import, int(),  array initializer
	$line=~ s/import.*$//;
	$line=~ s/\bint\b\((.*)\)/$1/;
	$line=~ s/(.*?)\[(\D\w*)\]/$1\[\$$2\]/;
	
	# translate #! line
    if ($line =~ /^#!/ && $. == 1) {
		print "#!/usr/bin/perl -w\n";
	# Blank & comment lines can be passed unchanged
    } elsif ($line =~ /^\s*(#|$)/) {
		print "$line\n";
	# translate break and continue
	} elsif ($line=~ s/^\s+break$/last;/){
		print "$line\n";
	} elsif ($line=~ s/^\s+next$/continue;/){
		print "$line\n";
	# handle stdin and stdout
	} elsif ($line =~ s/sys\.stdout\.write\((.*)\)/print $1;/){
		print "$line\n";
	} elsif ($line =~ s/\s*(.*?)\s*=.*?sys\.stdin\.readline\(\)/\$$1 = <STDIN>;/){
		print "$line\n";
	##handle iteration over sys.stdin (for line in sys.stdin)
	} elsif ($line =~ s/for (.*?) in sys\.stdin:/foreach \$$1 \(<stdin>\) {/){
			print "$line\n";
			$loop_no=$loop_no+1;
	## handle readlines()
	} elsif ($line=~ /\s*(.*?)\s*=\s*sys\.stdin\.readlines\(\)/){
		$array{$1}=1;
		print "my \@$1;\n";
		print "while (\$i=<STDIN>) {\n";
		print "    push \@$1, \$i;}\n";
		
    ##handle print statment
    } elsif ($line =~ /^\s*print/){
		#print outputs a new-line character by default
		$line =~ s/print\((.*?), end=''\)/print \$$1;/;
		$line =~ s/print\("(.*)"\)$/print \"$1\\n\";/;
		$line =~ s/print\("%[fds] (.*?)" % (.*)\)/print \"\$$2 $1\\n\";/;
		$line=~ s/^\s*print\(\)$/print "\\n";/;
		
		if ($line=~ /print\(([a-zA-Z_]\S*)\)/){
			if (exists($array{$1})){
				$line= "print \"\@$1\\n\";";
			} else { $line= "print \"\$$1\\n\";";}}
		
		if ($line=~ s/print\(\s*([a-zA-Z_]\S*)\s*([\+\-\*\/%]+.*)\)/$2/) {
			push(@temp, "\$$1");
			$line=~ s/([a-zA-Z_]\S*)+/\$$1/g;
			push(@temp, "$line");
			$line= join(' ',"print",@temp, ", \"\\n\";");}
		print "$line\n";
			
	
	##handle array
	} elsif ($line=~/\s*(.*?)\s*=\s*\[(.*?)\]/){
		$name=$1;
		$array{$1}=1;
		print "\@$name = ($2);\n";
	## handle simple sorting
	} elsif ($line=~ s/\s*(.*?)\s*=\s*sorted\((.*)\)/\@$1 = sort \@$2/){
		print "$line;\n";
		
	##handle append	/ pop with integer or variables argument	
	} elsif ($line =~ s/\s*(.*?)\.append\((".*?")\)$/push \@$1, $2;/){
			print "$line\n";
	} elsif ($line =~ s/\s*(.*?)\.append\((.*)\)$/push \@$1, \$$2;/){
			print "$line\n";
	} elsif ($line =~ s/\s*(.*?)\.pop\(()\)$/pop \@$1;/){
			print "$line\n";
	

##handle while/if loop multi line
	} elsif ($line=~ /(while|if|elif).*?:$/){
		$line=~ /\s*(.*?) (.*?):$/;
		$ifwhile=$1;
		$conditional=$2;
		$ifwhile=~ s/elif/elsif/;
	
		push(@temp, $ifwhile);
		$conditional=~ s/(\b(?!not|and|or)[a-zA-Z_]\S*)/\$$1/g;
		push(@temp, "($conditional){");
		
		$line= join(' ', @temp);
		print "$line\n";
		$loop_no= $loop_no+1;
		
	} elsif ($line=~ /\s*(else):$/){
		print "$1 {\n";
		$loop_no= $loop_no+1;
		
 ##handle while/if loop single line statement
    } elsif ($line=~/(while|if) (.*?):\s*(.*)$/) {
        $if_while=$1;
        $conditional=$2;
        $clauses=$3;
        @temp= split /;\s*/, $clauses;
		$conditional=~ s/(\b(?!not|and|or)[a-zA-Z_]\S*)/\$$1/g;

        print "$if_while \($conditional\) {\n";
        foreach $i (@temp) {
                $i=~ s/break/last/;
                $i=~ s/continue/next/;
				if ($i=~ /print/){
               		$i =~ s/print\("(.*)"\)$/print \"$1\\n\";/;
					$i =~ s/print\((.*?), end=''\)/print \$$1;/;
					$i =~ s/print\("%[fds] (.*?)" % (.*)\)/print \"\$$2 $1\\n\";/;
					$i=~ s/^\s*print\(\)$/print "\\n";/;
					$i=~ s/=\s*(\S+)\s*\/\/\s*(\d+)/=int($1\/$2)/;
					$i=~ s/print\(([a-zA-Z_]\S*)\)/print \"\$$1\\n\";/;
					
					if ($i=~ s/print\(\s*([a-zA-Z_]\S*)\s*([\+\-\*\/%]+.*)\)/$2/){
						push(@array, "\$$1");
						$i=~ s/([a-zA-Z_]\S*)+/\$$1/g;
						push(@array, "$i");
						$i= join(' ',"print",@array, ", \"\\n\";");
						
					} 
				} else {
					$i=~ s/([a-zA-Z_][a-zA-Z_0-9\(\)]*)+/\$$1/g;
					$i=~ s/=\s*(\S+)\s*\/\/\s*(\d+)/=int($1\/$2)/;
				}
		
         		print "    $i\n;";
    	}
        print "}\n";
		
 ##handle for loop
    } elsif ($line=~ /for/ ){
        $loop_no= $loop_no + 1;
		# handle range 2 argument
		if ($line=~ /for (.*?) in range\((.*?),\s*(.*?)\):/) {
			$var=$1;
			$first=$2;
			$sec=$3;
			if ($sec=~/^\d+$/){
				$sec= $sec -1;
			} else {
				$sec=~ s/([^ ]+)/\$$1 - 1/;
				$sec=~ s/([^ ]+) + (\d+)/\$$1/;
			}
        	print "foreach \$$var ($first..$sec) {\n";
		# handle range 1 argument
	
		} elsif ($line=~ /for (.*?) in range\((.*)\):/){
			$var=$1;
			$sec=$2;
			if ($sec=~/^\d+$/){
				$sec= $sec -1;
			} else {
				$sec= "\$$sec-1";
			}
			print "foreach \$$var (0..$sec) {\n";
		} else {
			$line=~ /for (.*?) in (.*):/;
			$var=$1;
			$sec=$2;
			print "foreach \$$var \(\@$sec\) {\n";
		}
			
	## handle string
	} elsif ($line=~ s/(.*?)\s*=\s*"(.*)"$/\$$1 = "$2";/){
		print "$line\n";
	##handle variables and integers
	} elsif ($line=~ /(.*?=[^"]+[\+\-\*\/%]*.*)/) {
		#identify variables and convert to $variable
		$line=~ s/([a-zA-Z_][a-zA-Z_0-9\(\)]*)+/\$$1/g;
		# translate from // to /
		$line=~ s/=\s*(\S+)\s*\/\/\s*(\d+)/=int($1\/$2)/;
		#translate array len()	
		if ($line=~ /\$len\((.*)\)/){
			if (exists($array{$1})){
				$line=~ s/\$len\((.*)\)/\@$1/;
			} else {
				$line=~ s/\$len\((.*)\)/length\(\$$1\)/;}}
			
		print "$line;\n";
			
	# Lines we can't translate are turned into comments
    } else {
        print "#$line\n";
    }
}

##closing bracket if $loop_no 
if ($loop_no){
        $loop_no = $loop_no -1;
        print "}\n";}

