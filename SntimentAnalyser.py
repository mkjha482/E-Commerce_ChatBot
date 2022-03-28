from textblob import TextBlob
y = ""
def main():
    outfile = open('data.txt', 'a')
    analysed_data = input("Enter data to be analysed")
    outfile.write(analysed_data+' ')
    outfile.close()
main()
def readfile():
    infile = open('data.txt','r')
    y = str(infile.read())
    print(y)
    edu = TextBlob(y)
    x = edu.sentiment.polarity
    # Negative =x<0 and Neutral =0 and Positive more than 0 and less than 1
    if x < 0:
        print("Negative")
    elif x == 0:
        print("neutral")
    elif x > 0 and x <= 1:
        print("Positive")
    infile.close()
readfile()
delete_data = open("data.txt","w")
delete_data.truncate()
delete_data.close()



