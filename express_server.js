const express = require('express');
const session = require('express-session');
const passport = require('passport');
const { Strategy } = require('passport-facebook');
const fetch = require('node-fetch');
require('dotenv').config();
const path = require('path');

const app = express();
const PORT = 3001;

passport.serializeUser(function (user, done) {
    done(null, user);
});
passport.deserializeUser(function (obj, done) {
    done(null, obj);
});

passport.use(
    new Strategy(
        {
            clientID: process.env.FACEBOOK_CLIENT_ID,
            clientSecret: process.env.FACEBOOK_CLIENT_SECRET,
            callbackURL: `http://localhost:3001/auth/facebook/callback`,
            enableProof: true
        },
        async (accessToken, refreshToken, profile, done) => {
            return done(null, { accessToken, profile });
        }
    )
);

app.use(
    session({
        secret: 'secret',
        resave: false,
        saveUninitialized: true,
    })
);
app.use(passport.initialize());
app.use(passport.session());

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'index.html'));
});


app.get('/auth/facebook', passport.authenticate('facebook', {
    scope: ['pages_show_list', 'instagram_basic', 'instagram_content_publish', 'instagram_manage_insights', 'business_management'],
}));

app.get('/auth/facebook/callback',
    passport.authenticate('facebook', { failureRedirect: '/' }),
    async (req, res) => {
        if (!req.user) {
            return res.redirect('/');
        }

        const accessToken = req.user.accessToken;
        const profile = req.user.profile;

        try {
            const igAccountsUrl = `https://graph.facebook.com/v14.0/me/accounts?fields=instagram_business_account{name,username,profile_picture_url}&access_token=${accessToken}`;
            const response = await fetch(igAccountsUrl);
            const data = await response.json();

            if (!data.data || data.data.length === 0) {
                throw new Error('No Instagram accounts found.');
            }

            const instagramAccounts = data.data
                .map(account => account.instagram_business_account)
                .filter(account => account);

            if (instagramAccounts.length === 0) {
                throw new Error('No Instagram accounts found.');
            }

            req.session.instagramAccounts = instagramAccounts;

            const instagramAccount = instagramAccounts[0];
            res.redirect(`http://localhost:5000/enter_post_id?username=${profile.displayName}&access_token=${accessToken}&ig_username=${instagramAccount.username}`);
        } catch (error) {
            res.status(500).send('<h1>Error fetching Instagram accounts</h1><p>Please try again later.</p>');
        }
    }
);

app.listen(PORT, () => {
    console.log(`Listening on http://localhost:${PORT}`);
});
