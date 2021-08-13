importClass(org.openqa.selenium.firefox.FirefoxDriver);
importClass(org.openqa.selenium.firefox.FirefoxProfile);
importClass(com.galenframework.utils.GalenUtils);
importClass(com.galenframework.browser.SeleniumBrowser);
importClass(org.openqa.selenium.WebDriver);
importClass(org.openqa.selenium.firefox.internal.ProfilesIni);
importClass(org.openqa.selenium.firefox.FirefoxOptions);

// Basic JavaScript browser factory
// Following the guide http://galenframework.com/docs/reference-galen-test-suite-syntax/
// Browser is set to reject all cookies

var pageUrl = args[0];
var size = GalenUtils.readSize(args[1]);

var profile = new FirefoxProfile();

profile.setPreference("network.cookie.cookieBehavior", 2)
var opts = new FirefoxOptions();
opts.setProfile(profile);


var browser = new SeleniumBrowser(new FirefoxDriver(opts));
browser.load(pageUrl);
browser.changeWindowSize(size);

browser;
