function getQuote(authors) {
    // Choose random author
    let author = authors[Math.floor(Math.random() * /*authors.length*/ 10)];

    // Get a new quote.
    let oldQuote = $('h2').text()
    let newQuote = author.quotes[Math.floor(Math.random() * author.quotes.length)];
    while (newQuote == oldQuote) {
        newQuote = author.quotes[Math.floor(Math.random() * author.quotes.length)];
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
            $('.button').addClass('active');
            $('.button').removeClass('waiting');
        })
    });
    console.clear();
    console.log(`\n"${newQuote}" \n\n${author.name}\n${author.title}\n`);
}

$(document).ready(function() {
    // Get new quote on button click.
    $('.active').click(function() {
        $(this).addClass('waiting');
        $(this).removeClass('active');
        $.getJSON("authors.json", getQuote);
    })
});
