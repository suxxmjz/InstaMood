# InstaMood

InstaMood is an application that analyzes your Instagram posts' comments. Just enter your post ID and see how your audience respond to your posts!

# How to use

1. follow this link to create a Facebook page that will be linked to the Instagram account https://help.instagram.com/570895513091465

2. create a Facebook developer account and follow this link to set it up https://superface.ai/blog/instagram-login

3. once you have the Facebook client ID and secret, add them to the .env file

4. run node express_server.js

5. run python app.py

6. go to http://localhost:3001/

7. authenticate using the Facebook account and the Instagram account linked to it

8. once authenticated, enter your Instagram post's shortcode from the post's URL

9. click Submit
  
10. your post's sentiment analysis will be available in both a pie chart for the sentiment ratios and a scatter plot for how sentiments evolve over time

11. click on Export Images to export the two graphs as .png files for future references

12. click Analyze another post to return to the previous page to enter another shortcode