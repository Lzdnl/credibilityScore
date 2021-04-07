importClass(org.openqa.selenium.firefox.FirefoxDriver);
importClass(org.openqa.selenium.firefox.FirefoxProfile);
importClass(com.galenframework.utils.GalenUtils);
importClass(com.galenframework.browser.SeleniumBrowser);
importClass(org.openqa.selenium.WebDriver);
importClass(org.openqa.selenium.firefox.internal.ProfilesIni);
importClass(org.openqa.selenium.firefox.FirefoxOptions);

var pageUrl = args[0];
var size = GalenUtils.readSize(args[1]);

var profile = new FirefoxProfile();
profile.addExtension(java.io.File, "i_dont_care_about_cookies-3.2.4-an+fx.xpi");


var opts = new FirefoxOptions();
opts.setProfile(profile);


var browser = new SeleniumBrowser(new FirefoxDriver(opts));
browser.load(pageUrl);
browser.changeWindowSize(size);

browser;
