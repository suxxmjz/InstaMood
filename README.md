# InstaMood

InstaMood is an application that analyzes your Instagram posts' comments. Just enter your post ID and see how your audience respond to your posts!

![image](https://github.com/suxxmjz/InstaMood/assets/92133996/db99bedf-3040-4495-9857-62e4901b7d7f)

# How to use

1. create a Facebook page using your Facebook account using https://www.facebook.com/pages/create/

2. change the Instagram account that you want your Facebook page to be linked to into an Instagram Business account using https://help.instagram.com/502981923235522

3. connect the Instagram Business account to your Facebook page using https://superface.ai/blog/instagram-setup?utm_source=blog&utm_medium=link&utm_campaign=instagram-login

4. create a Facebook developer account and follow this link to set it up https://superface.ai/blog/instagram-login

5. once you have the Facebook App ID and secret, add them to the .env file

6. in your IDE run ```node express_server.js``` in one terminal

7. in another terminal, run ```python app.py```

8. go to http://localhost:3001/

9. authenticate using the Facebook account and the Instagram account linked to it

10. once authenticated, enter your Instagram post's shortcode from the post's URL

![image](https://github.com/suxxmjz/InstaMood/assets/92133996/0dfe2098-ac62-4b4d-832e-fb98bb975c04)

![image](https://github.com/suxxmjz/InstaMood/assets/92133996/073231ef-4250-4f4c-9925-c799b943bfa4)

9. click Submit
  
10. your post's sentiment analysis will be available in both a pie chart for the sentiment ratios and a scatter plot for how sentiments evolve over time

![Post Dashboard - Google Chrome 2024-06-11 00-28-17 - Trim](https://github.com/suxxmjz/InstaMood/assets/92133996/db6f5dcc-de92-4612-8c26-f4b09f05c114)

11. click on Export Images to export the two graphs as .png files for future references

12. click Analyze another post to return to the previous page to enter another shortcode
