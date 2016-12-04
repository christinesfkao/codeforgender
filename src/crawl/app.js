var Promise = require('bluebird');
var request = require('request');
var fs = require('fs');
var async = require('async');
var cheerio = require('cheerio');
var fs = require('fs');

var pttBase = 'https://www.ptt.cc';
var gossipingHome = '/bbs/Gossiping/index';
var ext = '.html';

process.on('uncaughtException', function (err) {
  console.log('Caught exception: ' + err);
});

var pageFetcher = async.queue(function(task, callback) {
    postDate = new Date(parseInt((task.split('.')[1]) + '000'));
    postYear = postDate.getFullYear();
    filePath = 'data/' + postYear + '/' + task.split('/')[3];
    if(!fs.existsSync('data/' + postYear)){
        fs.mkdirSync('data/' + postYear);
        console.log('year start', postYear);
    }
    if(fs.existsSync(filePath)) return callback();
    request({
        url: pttBase + task,
        headers: {
            Cookie: 'over18=1'
        }
    }).pipe(fs.createWriteStream(filePath).on('finish', function() {
        callback()
    }));
}, 10);

var indexFetcher = async.queue(function(task, callback) {
    request({
        url: pttBase + gossipingHome + task + ext,
        headers: {
            Cookie: 'over18=1'
        }
    }, function(err, res, body) {
        if(err) return console.log(err);
        var $ = cheerio.load(body);
        $('.title').each(function(i, elem) {
            var lnk = $(this).children('a').attr('href');
            pageFetcher.push(lnk);
        });
        if(task % 50 == 0) console.log('page', task);
        callback();
    });
}, 5);

request({
    url: pttBase + gossipingHome + ext,
    headers: {
        Cookie: 'over18=1'
    }
}, function(err, res, body) {
    if(err) return console.log(err);
    var $ = cheerio.load(body);
    var maxpage = 1;
    $('a.btn.wide').each(function(i, elem) {
        if($(this).text() == '‹ 上頁') {
            maxpage += parseInt($(this).attr('href').replace(/\D+/g, ''));
        }
    });
    console.log(maxpage);
    for(var i = 1; i <= maxpage; i++) {
        indexFetcher.push(i);
    }
    // async.parallelLimit(, 10)
});
