require('dotenv').config();

const express = require('express');
const SpotifyWebApi = require('spotify-web-api-node')
const path = require('path');


const app = express();
const port = 3000;

const spotifyApi = new SpotifyWebApi({
    clientId: process.env.CLIENT_ID,
    clientSecret: process.env.CLIENT_SECRET,
    redirectUri:process.env.REDIRECT_URL
})


//get user to log in and request scopes, can alter scopes requested later
app.get('/login', (req, res) => {
    const scopes = ['user-read-private', 'user-read-email', 'user-library-read', 
    'user-library-modify', 'user-read-playback-state', 'user-modify-playback-state', 'user-top-read',
    'playlist-modify-public', 'playlist-modify-private'];

    res.redirect(spotifyApi.createAuthorizeURL(scopes));
})


app.get('/', (req, res) => {
    // res.sendFile(path.join(__dirname, 'index.html'));
    const error = req.query.error;
    const code = req.query.code;
    const state = req.query.state;

    if (error) {
        console.error('Error:', error);
        res.send(`Error: ${error}`);
        return;
    }

    // If no error, exchange authorization code for access token
    spotifyApi.authorizationCodeGrant(code).then(data => {
        const accessToken = data.body['access_token']; // Corrected typo here
        const refreshToken = data.body['refresh_token'];
        const expiresIn = data.body['expires_in'];

        // Set access token and refresh token
        spotifyApi.setAccessToken(accessToken);
        spotifyApi.setRefreshToken(refreshToken);

        // Print out access token and refresh token in console
        console.log('Access Token:', accessToken);
        console.log('Refresh Token:', refreshToken);

        // Refresh access token when it expires
        setTimeout(async () => {
            const data = await spotifyApi.refreshAccessToken();
            const accessTokenRefreshed = data.body['access_token'];
            spotifyApi.setAccessToken(accessTokenRefreshed);
            console.log('Access Token Refreshed:', accessTokenRefreshed);
        }, expiresIn * 1000); // Convert expiresIn to milliseconds

        // Redirect to the search page
        res.redirect('/search');
    }).catch(error => {
        console.error('Error:', error);
        res.send('Error getting token');
    });
});



// app.get('/search', (req,res) =>{
//     const {q} = req.query;
//     spotifyApi.searchTracks(q).then(searchData=>{
//         const trackUri = searchData.body.tracks.items[0].uri;
//         res.send({uri:trackUri}); 
//         console.log({uri:trackUri});
//     }).catch(err=>{
//         res.send(`Error playing ${err}`);
//     })
// })



//works well
// app.get('/search', (req, res) => {
//     const { q } = req.query;
//     if (!q) {
//         res.sendFile(path.join(__dirname, 'search.html')); // Render the search form if no query is provided
//         return;
//     }
//     spotifyApi.searchTracks(q).then(searchData => {
//         const trackUri = searchData.body.tracks.items[0].uri;
//         res.send({ uri: trackUri });
//         console.log({ uri: trackUri });
//     }).catch(err => {
//         res.send(`Error playing ${err}`);
//     });
// });



///redirect straight to play
app.get('/search', (req, res) => {
    const { q } = req.query;
    if (!q) {
        res.sendFile(path.join(__dirname, 'search.html')); // Render the search form if no query is provided
        return;
    }
    console.log(q);
    spotifyApi.searchTracks(q).then(searchData => {
        const trackUri = searchData.body.tracks.items[0].uri;
        // Redirect to the play page with the track URI as a query parameter
        res.redirect(`/play?uri=${encodeURIComponent(trackUri)}`);
    }).catch(err => {
        res.send(`Error searching for tracks: ${err}`);
    });
});



//working 
// app.get('/play', (req, res) => {
//     const { uri } = req.query;
//     spotifyApi.getMyDevices().then(data => {
//         const devices = data.body.devices;
//         // res.json(devices);
//         if (devices.length > 0) {
//             // Devices found, display the list
//             let deviceList = '';
//             devices.forEach(device => {
//                 deviceList += `${device.name} (${device.type})\n`;
//             });
//             deviceList = 'Available devices:\n' + deviceList;
//             res.send(deviceList);

//             // Start playback on the first device in the list
//             const deviceId = devices[0].id;
//             spotifyApi.play({ uris: [uri], device_id: deviceId }).then(() => {
//                 res.send('Playback started on ' + devices[0].name);
//             }).catch(err => {
//                 res.send(`Error playing track: ${err.message}`);
//             });
//         } else {
//             // No active devices found, inform the user
//             res.send('No active devices found. Please open Spotify on your device and try again.');
//         }

//     }).catch(err => {
//         res.send(`Error getting devices: ${err.message}`);
//     });
// });

//testing
app.get('/play', (req, res) => {
    const { uri } = req.query;

    spotifyApi.getMyDevices().then(data => {
        const devices = data.body.devices;
        if (devices.length > 0) {
            // Start playback on the first device in the list
            const deviceId = devices[0].id;
            spotifyApi.play({ uris: [uri], device_id: deviceId }).then(() => {
                // Playback started successfully, now get recommendations
                // Call the recommendation logic here
                getRecommendationsAndRespond(res);
                res.send(res);
            }).catch(err => {
                res.send(`Error playing track: ${err.message}`);
            });
        } else {
            // No active devices found, inform the user
            res.send('No active devices found. Please open Spotify on your device and try again.');
        }
    }).catch(err => {
        res.send(`Error getting devices: ${err.message}`);
    });
});

// Function to get recommendations and respond to the client
function getRecommendationsAndRespond(res) {
    Promise.all([
        spotifyApi.getMyTopArtists({ limit: 5 }), // Get your top 5 artists
        spotifyApi.getMyTopTracks({ limit: 5 }), // Get your top 5 tracks
    ]).then(([topArtists, topTracks]) => {
        // Extract necessary information from the response
        const seedArtists = topArtists.body.items.map(artist => artist.id); // Get the IDs of your top artists
        const seedTracks = topTracks.body.items.map(track => track.uri); // Get the URIs of your top tracks

        // Retrieve additional information about the top artists and tracks
        const artistNames = topArtists.body.items.map(artist => artist.name); // Get the names of your top artists
        const trackNames = topTracks.body.items.map(track => track.name); // Get the names of your top tracks
        const artistGenres = topArtists.body.items.map(artist => artist.genres); // Get the genres of your top artists

        // Combine all genres into a single array
        const seedGenres = artistGenres.flat().filter((genre, index, self) => self.indexOf(genre) === index);

        // Now you have the necessary information to use as seed parameters for recommendations
        console.log('Seed Artists:', seedArtists);
        console.log('Seed Tracks:', seedTracks);
        console.log('Top Artist Names:', artistNames);
        console.log('Top Track Names:', trackNames);
        console.log('Top Artist Genres:', artistGenres);
        console.log('Seed Genres:', seedGenres);

        // Use the retrieved seed parameters to get recommendations
        spotifyApi.getRecommendations({
            seed_artists: seedArtists,
            seed_tracks: seedTracks,
            seed_genres: seedGenres, // Add seed genres to the recommendation parameters
            limit: 10 // Limit the number of recommendations to 10
        }).then(data => {
            const recommendations = data.body.tracks.map(track => track.name); // Get the names of the recommended tracks
            console.log('Recommendations:', recommendations);

            // Send the response with the recommendations
            res.send({ recommendations }); // Send recommendations as JSON object
        }).catch(error => {
            console.error('Error getting recommendations:', error);
            res.status(500).send('Error getting recommendations');
        });
    }).catch(error => {
        console.error('Error getting top artists and tracks:', error);
        res.status(500).send('Error getting top artists and tracks');
    });
}




// app.get('/recommend', (req, res) =>{
//     const { uri } = req.query;
//     spotifyApi.getMyDevices().then(data => {
//     const devices = data.body.devices;
//     if (devices.length > 0) {
//         // Devices found, display the list
//         let deviceList = '';
//         devices.forEach(device => {
//             deviceList += `${device.name} (${device.type})\n`;
//         });
//         deviceList = 'Available devices:\n' + deviceList;
//         res.send(deviceList);

//         // Start playback on the first device in the list
//         const deviceId = devices[0].id;
//         spotifyApi.play({ uris: [uri], device_id: deviceId }).then(() => {
//             // Playback started successfully
//             console.log('Playback started on ' + devices[0].name);
//         }).catch(err => {
//             console.error(`Error playing track: ${err.message}`);
//         });
//     } else {
//         // No active devices found, inform the user
//         res.send('No active devices found. Please open Spotify on your device and try again.');
//     }

//     // Use the Spotify Web API's getMyTopArtists, getMyTopTracks, and getMySavedTracks endpoints to get your top artists, tracks, and saved tracks
//     return Promise.all([
//         spotifyApi.getMyTopArtists({ limit: 5 }), // Get your top 5 artists
//         spotifyApi.getMyTopTracks({ limit: 5 }) // Get your top 5 tracks
//     ]);
//     }).then(([topArtists, topTracks]) => {
//     // Extract necessary information from the response
//     const seedArtists = topArtists.body.items.map(artist => artist.id); // Get the IDs of your top artists
//     const seedTracks = topTracks.body.items.map(track => track.uri); // Get the URIs of your top tracks
//     // You can also extract genres from top artists if needed

//     // Now you have the necessary information to use as seed parameters for recommendations
//     console.log('Seed Artists:', seedArtists);
//     console.log('Seed Tracks:', seedTracks);
// }).catch(error => {
//     console.error('Error getting top artists and tracks:', error);
//     res.status(500).send('Internal server error');
// });


// });


// app.get('/play', (req, res) => {

//     const { deviceId, uri } = req.query;
//     if (!deviceId) {
//         res.status(400).send('No device selected.');
//         return;
//     }

//     spotifyApi.play({ uris: [uri], device_id: deviceId })
//         .then(() => {
//             res.sendStatus(200); // Playback started successfully
//         })
//         .catch(error => {
//             if (error.statusCode === 404 && error.body.error.reason === 'NO_ACTIVE_DEVICE') {
//                 res.status(400).send('No active device found. Please open Spotify on your device and try again.');
//             } else {
//                 console.error('Error playing track:', error);
//                 res.status(500).send('Error starting playback. Please try again.');
//             }
//         });
// });





app.listen(port,()=>{
    console.log(`Listening at http://localhost:${port}/login`)
})