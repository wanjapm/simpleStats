#!/usr/bin/env python
# coding: utf-8

# In[2]:


import gzip
path = "/mnt/c/Users/user/Downloads/amazon_reviews_us_Gift_Card_v1_00.tsv.gz"
# calling this path from within linux and not windows
f = gzip.open(path,'rt')


# In[3]:


import csv
reader = csv.reader(f, delimiter='\t')


# In[4]:


header = next(reader) # get the header(fields) of the tsv file as a list


# In[5]: convert strings to number and boolean fields where possible


dataset = [] # we want to create a list of dictionaries
for line in reader:
    d = dict(zip(header,line))
    for field in ['helpful_votes', 'star_rating', 'total_votes']:
        d[field] = int(d[field]) # convert string to number for number fields
    for field in ['verified_purchase', 'vine']:
        if d[field] == 'Y':
            d[field] = True # convert string to boolean for boolean fields
        else:
            d[field] = False
    dataset.append(d) # dataset is a list of dictionaries


# In[10]: What is the average star rating?


# Average rating = get all ratings / number of ratings
ratings = [d['star_rating'] for d in dataset]
print(f"Average Gift Card Rating: {sum(ratings) / len(ratings):2f}")


# In[12]: What is the distribution of star ratings?


# Rating distribution e.g how many ratings for 1 are there, for 2, for 3 and so on.
ratingsCount = {1:0, 2:0, 3:0 , 4:0 , 5:0}
for d in dataset:
    ratingsCount[d['star_rating']] +=1
    


# In[13]:


ratingsCount


# In[14]:


# The above solution works if there are few possibilities
from collections import defaultdict
ratingsCount = defaultdict(int)
for d in dataset:
    ratingsCount[d['star_rating']] +=1


# In[21]:


ratingsCount


# In[22]: What fractions of purchases are verified?


verifiedCounts = defaultdict(int)
for d in dataset:
    verifiedCounts[d['verified_purchase']] +=1


# In[23]:


verifiedCounts


# In[25]: Which products are the most popular (purchases)?


productCounts = defaultdict(int)
for d in dataset:
    productCounts[d['product_id']] +=1

counts = [(productCounts[p],p) for p in productCounts] 
# p=key i.e {product_id:count} counts= (count,product_id)
 # printing print(dict) will print the key
 # we are sorting by the first value in tuple - the counts that is why we made counts first value in list
 # the last 10 items in list - the 10 highest
counts.sort()
counts[-10:]


# In[30]: Which products have the highest average ratings?


# average rating for each product
# get the ratings for each product
# divide ratings by the number of ratings
ratingsPerProduct = defaultdict(list)


# In[34]: What is the average rating for each product?


for d in dataset:
    ratingsPerProduct[d['product_id']].append(d['star_rating'])


# In[35]:


averageRatingsPerProduct = {}
for p in ratingsPerProduct:
    averageRatingsPerProduct[p] = sum(ratingsPerProduct[p]) / len(ratingsPerProduct[p])


# In[36]: What are the top rated products?
# we would like to get reasonably popular products i.e. where number of product reviews > 50
# if a product has one rating only and the rating is 5 it will be highly rated yet only one review

topRated  = [(averageRatingsPerProduct[p],p) for p in averageRatingsPerProduct if len(ratingsPerProduct[p]) > 50 ]


# In[37]:


topRated.sort()
topRated[-10:]


# In[58]: Who are the most active users?


# Most active users
activeUserCount = defaultdict(int)


# In[59]:


for d in dataset:
    activeUserCount[int(d['customer_id'])] +=1


# In[76]:


counts = [(activeUserCount[u],u) for u in activeUserCount if activeUserCount[u] > 3]
counts.sort()
counts[-10:]
#activeUserCount


# In[84]:


# most commonly used words in the reviews
# split the words and count the words
reviewWords = defaultdict(int)
for d in dataset:
    for word in d['review_body'].split():
        word.replace('!','').replace('.','').replace('!','').strip().replace("'","").replace("&","")
        if len(word)>3: # can have a list of words to filter out here
            reviewWords[word]+=1

counts = [ (reviewWords[word], word) for word in reviewWords]
counts.sort()
counts[-10:]


# In[88]:


# difference in average rating between  verified and non-verified purchase
# get average rating for verified  and non-verified purchases
purchasesRatings = defaultdict(list)


# In[90]:


for d in dataset:
    if d['verified_purchase']:
        purchasesRatings['verified'].append(d['star_rating'])
    else:
        purchasesRatings['non-verified'].append(d['star_rating'])

for r in purchasesRatings:
    print("{} average ratings: {:2f} ".format(r.title(),sum(purchasesRatings[r])/len(purchasesRatings[r]) ))


# In[ ]:




