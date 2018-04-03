/*
FreeCodeCamp Criteria: https://www.freecodecamp.org/challenges/use-the-twitchtv-json-api
Working with the Twitch API: https://daveconway.net/blog/entry/67/making-requests-from-javascript-to-the-new-twitch-helix-api
Twitch API documentation: https://dev.twitch.tv/docs/api/reference/
Starcraft I, game_id=11989
Starcraft II, game_id=490422
*/

const OFFLINE = 0;
const ONLINE = 1;

let trackedCasters = ["StarCraft", "OgamingSC2", "GSL", "ESL_SC2", "BaseTradeTV", "Wardiii",
    "RoXKISPomi", "Crank", "StarLadder_SC2_RU", "TaKeTV", "wesg_sc2", "ESL", "BlizzardZHTW"
];

let casterObjects = [];

$(document).ready(function() {
    // Construct caster objects.
    $.ajax({
        type: "GET",
        url: "https://api.twitch.tv/helix/users",
        dataType: "json",
        headers: { "Client-ID": "gnb2ffv3rmyk6km2stfqgpf68mribo" }, stream is online . same with offline streamer.
        data: $.param({ login: trackedCasters }, true),
        success: (response) => {
            trackedCasters = [];
            for (let i = 0; i < response['data'].length; i++) {
                // Create caster object.
                let caster = {}
                caster.id = response['data'][i].id;
                caster.img = response['data'][i].profile_image_url;
                caster.name = response['data'][i].display_name;
                caster.info = response['data'][i].description;
                casterObjects.push(caster);

                trackedCasters.push(caster.id);

                // Add caster to index.html.
                let html_ = `<div id="${caster.id}" class="caster"><div><img class="img-fluid" src="${caster.img}" alt="${caster.info}" /></div><div id="name">${caster.name}</div></div>`;
                $('#container').append(html_);
            }
            console.log(trackedCasters);
        },
        error: (response) => { console.log("Error", response); }
    });



    // Get stream data.
    $.ajax({
        type: "GET",
        url: "https://api.twitch.tv/helix/streams",
        dataType: "json",
        headers: { "Client-ID": "gnb2ffv3rmyk6km2stfqgpf68mribo" },
        data: $.param({ login: trackedCasters[0] }, true),
        success: (response) => {
            console.log("Success", response)
            // for (let i = 0; i < response['data'].length; i++) {
            //     // Create caster object.
            //     let caster = {}
            //     caster.id = response['data'][i].id;
            //     caster.img = response['data'][i].profile_image_url;
            //     caster.name = response['data'][i].display_name;
            //     caster.info = response['data'][i].description;
            //     casterObjects.push(caster);

            //     // Add caster to index.html.
            //     let html_ = `<div id="${caster.id}" class="caster"><div><img class="img-fluid" src="${caster.img}" alt="${caster.info}" /></div><div id="name">${caster.name}</div></div>`;
            //     $('#container').append(html_);
            // }
        },
        error: (response) => { console.log("Error", response); }
    });
});


// for (let caster of casterObjects) {
//     let html_ = `<div id="${caster.id}" class="caster"><div><img class="img-fluid" src="${caster.img}" alt="${caster.info}" /></div><div id="name">${caster.name}</div></div>`;
//     $('#container').append(html_);
// }