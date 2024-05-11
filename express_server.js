const express = require('express');
const session = require('express-session');
const passport = require('passport');
const { Strategy } = require('passport-facebook');
const path = require('path');
const { SuperfaceClient } = require('@superfaceai/one-sdk');
require('dotenv').config();

const app = express();
const PORT = 3000;
const superface = new SuperfaceClient();

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
            callbackURL: `${process.env.BASE_URL}/auth/facebook/callback`,
            enableProof: true
        },
        async (accessToken, refreshToken, profile, done) => {
            done(null, { accessToken, profile });
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
    res.send('<h1>Welcome to App</h1><a href="/auth/facebook">Login with Facebook</a>');
});

app.get('/auth/facebook', passport.authenticate('facebook', {
    scope: ['pages_show_list', 'instagram_basic', 'instagram_content_publish'],
}));

app.get('/auth/facebook/callback',
    passport.authenticate('facebook', { failureRedirect: '/' }),
    async (req, res) => {
        try {
            const accessToken = req.user.accessToken;
            const profileUseCase = await superface.getProfile('social-media/publishing-profiles@1.0.1');
            const result = await profileUseCase.getUseCase('GetProfilesForPublishing').perform({}, {
                provider: 'instagram',
                parameters: {
                    accessToken,
                },
            });

            const profiles = result.unwrap();

            res.send(`
                <h1>Authentication succeeded</h1>
                <h2>User data</h2>
                <pre>${JSON.stringify(req.user, undefined, 2)}</pre>
                <h2>Instagram profiles</h2>
                <pre>${JSON.stringify(profiles, undefined, 2)}</pre>
            `);
            next();
        } catch (err) {
          next(err);
        }
      }
    );

app.listen(3000, () => {
    console.log(`Listening on ${process.env.BASE_URL}`);
});
