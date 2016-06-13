#!/usr/bin/python

import psycopg2

try:
   conn = psycopg2.connect(database="search_bot", user="postgres", password="deep", host="127.0.0.1", port="5432")
   print "Opened database successfully"

   cur = conn.cursor()
   input_string = raw_input("Input your query.. ")
   #print input_string

   try:
      cur.execute("SELECT id, like_score, reads, word_count, created_at, reply_to_post_number, incoming_link_count, raw, is_doc, fitness, ts_rank_cd(indexed_data, query, 8|1) AS rank FROM posts, plainto_tsquery('english', %s) query WHERE indexed_data @@ query and created_at >= '2014-01-01' ORDER BY rank DESC LIMIT 15;", [input_string])

      rows = cur.fetchall()
      for row in rows:
         iden = row[0]  
         read = row[2]
         likes = row[1]
         word = row[3]
         create_date = row[4]
         reply = row[5]
         link = row[6]
         data = row[7]
         doc = row[8]
         fit = row[9]
         rank = row[10]
         print "ID = ", iden
         print "Likes : ", likes 
         print "Reads : ", read 
         print "Word Count : ", word 
         print "Created at : ", create_date
         print "reply_to_post_number : ", reply
         print "Incoming_link_count : ", link 
         print "Rank : ", rank
         print "Is this a doc : ", doc
         print "Post Data : " , data
         print "\n"

         fit1 = float(input("Enter a fitness value (0-10): "))
         while(fit1 > 10 or fit1 < 0):
            fit1 = float(input("Enter a correct value : "))
         fit1  = fit1/10

         if(fit == 0.0):
            fit = fit1
         else:
            fit = (fit + fit1)/2

         try:
            cur.execute("UPDATE posts SET fitness = %s WHERE id = %s;", [fit, iden])
            #print "Fitness value set";
   
         except :
            print e;

         print "________________________________________________________________________________________________________", "\n"

      '''ans = input("Do you wish to enter an answer of your own? (y/n) :")
      if(ans == 'y'):
         ans_string = raw_input("Enter your answer : \n")
         word1 = len(ans_string.split())

         fit2 = float(input("Enter a fitness value for this answer (0-10): "))
         while(fit2 > 10 or fit2 < 0):
            fit2 = float(input("Enter a correct value : "))
         fit2 = fit2/10

         try:
            cur.execute("INSERT INTO posts (raw, reply_to_post_number, incoming_link_count, reads, like_score, word_count, is_doc, created_at, fitness) VALUES (%s, 0, 0, 0, 0, %s, 0, now(), %f);", [ans_string, word1, fit2])    
            conn.commit()
            print "Inserted successfully!"
         except:
            conn.rollback()
            print "Error!"'''


      conn.commit()
      conn.close()

   except:
      print "Cannot read posts table. Error : ", e
	
except:  
	print "Hello ..  Unable to connect to database."

