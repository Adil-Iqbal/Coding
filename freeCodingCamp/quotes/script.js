// Retrieves value of URL parameter.
function getPageParameters(pageParameter) {
    let allParameters = window.location.search.substring(1).split("&");
    for (param of allParameters) {
        param = param.split("=");
        if (param[0] == pageParameter) {
            param[1] = parseInt(param[1]);
            if (typeof param[1] === "number") {
                return param[1];
            }
        }
    }
    return undefined;
}
// Global variables.
let authorIndex = getPageParameters('a');
let quoteIndex = getPageParameters('q');
let tweet;
// Updates tweet button.
function setTweet() {
    // Construct quote URL. 
    let baseURL = window.location.href.split("?")[0];
    let a = "?a=" + authorIndex;
    let q = "%26q=" + quoteIndex;
    let url = baseURL + a + q;
    // Construct Tweet.
    tweet = `USA! USA! ${url} %23aaqm`;
    // Apply tweet to twitter button.
    $('#tweet').attr('href', 'https://twitter.com/intent/tweet?text=' + tweet);
    // Update URL in address bar.
    url = decodeURIComponent(url);
    window.history.pushState(undefined, undefined, url);
}
// Set to default quote.
function setDefault() {
    authorIndex = 2;
    quoteIndex = 10;
    setTweet();
    let quote = "Differences in political opinion are as unavoidable as, to a certain point, they may perhaps be necessary.";
    let authorName = "George Washington";
    let authorTitle = "First President of the United States";
    console.clear();
    console.log(`\n"${quote}" \n\n${authorName}\n${authorTitle}\n\n${tweet}`);
}
// Auto-formats alert messages.
function sendMessage(message = false) {
    let msg = "Our sincerest apologies...\n";
    if (message) {
        msg += "\n" + message.toString() + "\n";
    }
    alert(msg);
}
// JQUERY...
$(document).ready(function() {
    // On page load...
    $.getJSON("authors.json", (data) => {
        // Clean JSON data.
        data = data.filter(x => x.hasOwnProperty('quotes'));
        // Check if a specific author was requested.
        if (authorIndex === undefined) {
            if (quoteIndex !== undefined) {
                sendMessage("We cannot retrieve a quote unless we know it's author.");
            }
            setDefault();
            return;
        }
        // Check if author exists.
        let author = data[authorIndex];
        if (author === undefined) {
            sendMessage("We could not find that author.");
            setDefault();
            return;
        }
        // Check if a specific quote was requested.
        let quote;
        if (quoteIndex === undefined) {
            quoteIndex = Math.floor(Math.random() * author.quotes.length);
            quote = author.quotes[quoteIndex];
        } else {
            // Check if quote exists.
            quote = author.quotes[quoteIndex];
            if (quote === undefined) {
                sendMessage("The quote you requested was not found.\nWe have selected another quote from this author.");
                quoteIndex = Math.floor(Math.random() * author.quotes.length);
                quote = author.quotes[quoteIndex];
            }
        }
        // Check if quote is the same as default quote.
        let oldQuote = $('h2').text()
        if (quote == oldQuote) {
            setDefault();
            return;
        }
        // Change credit.
        let oldCredit = $('h3').html()
        let newCredit = `<b>${author.name}</b><br>${author.title}`;
        if (newCredit != oldCredit) {
            $('h3').html(newCredit);
        }
        // Change quote.
        $('h2').html(quote);
        setTweet();
        console.clear();
        console.log(`\n"${quote}" \n\n${author.name}\n${author.title}\n\n${tweet}`);
    });
    // If 'Another' button is clicked...
    $('.active').click(function() {
        $(this).addClass('waiting');
        $(this).removeClass('active');
        $.getJSON("authors.json", (data) => {
            // Clean JSON data.
            data = data.filter(x => x.hasOwnProperty('quotes'));
            // Choose random author.
            authorIndex = Math.floor(Math.random() * data.length);
            let author = data[authorIndex];
            // Get a random quote from that author.
            quoteIndex = Math.floor(Math.random() * author.quotes.length)
            let newQuote = author.quotes[quoteIndex];
            // Make sure the new quote is not the same as the last one.
            let oldQuote = $('h2').text()
            while (newQuote == oldQuote) {
                quoteIndex = Math.floor(Math.random() * author.quotes.length)
                newQuote = author.quotes[quoteIndex];
            }
            // Change credit.
            let oldCredit = $('h3').html()
            let newCredit = `<b>${author.name}</b><br>${author.title}`;
            if (newCredit != oldCredit) {
                $('h3').fadeOut(800, function() {
                    $(this).html(newCredit).fadeIn(800);
                });
            }
            // Change quote.
            $('h2').fadeOut(800, function() {
                $(this).html(newQuote).fadeIn(800, function() {
                    // Reactivate button when done.
                    $('.button').addClass('active');
                    $('.button').removeClass('waiting');
                })
            });
            setTweet();
            console.clear();
            console.log(`\n"${newQuote}" \n\n${author.name}\n${author.title}\n\n${tweet}`);
        });
    })
});
