let trackedCasters = ["StarCraft", "OgamingSC2", "GSL", "ESL_SC2", "BaseTradeTV", "Wardiii",
    "RoXKISPomi", "Crank", "StarLadder_SC2_RU", "TaKeTV", "wesg_sc2", "ESL", "BlizzardZHTW"
];

let objArray = [];

function makeURL(type, name) {
    return 'https://wind-bow.gomix.me/twitch-api/' + type + '/' + name + '?callback=?';
};

function sortByStatus(caster1, caster2) {
    if (caster1.status === 'online' && caster2.status === 'offline') {
        return -1;
    } else if (caster1.status === 'offline' && caster2.status === 'online') {
        return 1;
    } else {
        return 0;
    }
}

function populateContainer(limited) {
    let showArray;
    if (limited) {
        showArray = objArray.filter(caster => caster.status === 'online');
    } else {
        showArray = objArray.sort(sortByStatus);
    }
    $('#container').empty();
    for (let caster of showArray) {
        let html = `<a href="${caster.url}" target="_blank">
        <div class="caster ${caster.status}">
                		<div>
                			<img class="img-fluid" src="${caster.logo}" alt="${caster.name}" />
                		</div>
                		<div id="name">
                			${caster.name}
            			</div>
            		</div>
            		</a>`;
        $('#container').append(html);
    }
}

function swapButton(limited) {
    if (limited) {
        $('.limit').removeClass('showAll');
        $('.limit').addClass('liveNow');
        $('.limit').html('Live Now!');

    } else {
        $('.limit').removeClass('liveNow');
        $('.limit').addClass('showAll');
        $('.limit').html('Showing All');
    }
}

function buttonClicked(limit) {
    swapButton(limited = limit);
    populateContainer(limited = limit);
}


function getChannelInfo() {
    for (let login of trackedCasters) {
        $.getJSON(makeURL("streams", login), (data) => {
            let status = "online";
            if (data.stream === null || data.stream === undefined) {
                status = "offline";
            }
            $.getJSON(makeURL("channels", login), (data) => {
                let logo = data.logo != null ? data.logo : "https://dummyimage.com/75x75/ecf0e7/5c5457.jpg&text=%20N/A%20";
                let name = data.display_name != null ? data.display_name : login;
                objArray.push({
                    name: data.display_name != null ? data.display_name : login,
                    logo: data.logo != null ? data.logo : "https://dummyimage.com/75x75/ecf0e7/5c5457.jpg&text=%20N/A%20",
                    status: status,
                    url: "https://www.twitch.tv/" + login
                })
            })
        });
    }
}


$(document).ready(() => {
    getChannelInfo();
    let limit = false;
    $('.limit').click(() => {
        buttonClicked(limit);
        limit = !limit;
    });
    let timer = setInterval(function() {
        if ($('#container').contents().length !== trackedCasters.length) {
            buttonClicked(false);
            // console.log("Hey!");
            if ($('#container').contents().length === trackedCasters.length) {
                clearTimeout(timer);
            }
        }
    }, 1000);
})