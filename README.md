# InstaMood

InstaMood is an application that analyzes your Instagram posts' comments. Just enter your post ID and see how your audience respond to your posts!

![image](https://github.com/suxxmjz/InstaMood/assets/92133996/db99bedf-3040-4495-9857-62e4901b7d7f)

# How to use

1. follow this link to create a Facebook page that will be linked to the Instagram account https://help.instagram.com/570895513091465

2. create a Facebook developer account and follow this link to set it up https://superface.ai/blog/instagram-login

3. once you have the Facebook client ID and secret, add them to the .env file

4. run node express_server.js

5. run python app.py

6. go to http://localhost:3001/

7. authenticate using the Facebook account and the Instagram account linked to it

8. once authenticated, enter your Instagram post's shortcode from the post's URL

![image](https://github.com/suxxmjz/InstaMood/assets/92133996/0dfe2098-ac62-4b4d-832e-fb98bb975c04)

![image](https://github.com/suxxmjz/InstaMood/assets/92133996/073231ef-4250-4f4c-9925-c799b943bfa4)

9. click Submit
  
10. your post's sentiment analysis will be available in both a pie chart for the sentiment ratios and a scatter plot for how sentiments evolve over time

![Post Dashboard - Google Chrome 2024-06-11 00-28-17 - Trim](https://github.com/suxxmjz/InstaMood/assets/92133996/db6f5dcc-de92-4612-8c26-f4b09f05c114)

11. click on Export Images to export the two graphs as .png files for future references

12. click Analyze another post to return to the previous page to enter another shortcode
