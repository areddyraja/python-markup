/**
 * AngularJS Tutorial 1
 * @author Nick Kaye <nick.c.kaye@gmail.com>
 */

/**
 * Main AngularJS Web Application
 */
var app = angular.module('tutorialWebApp', [
  'ngRoute', 'ngAnimate','ui.bootstrap','ngResource', 'ngMessages','mgcrea.ngStrap'
]);

/**
 * Configure the Routes
 */
app.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
    // Home
    .when("/", {templateUrl: "partials/home.html", controller: "CarouselDemoCtrl"})
    .when("/cloud", {templateUrl: "partials/cloud-services.html", controller: "PageCtrl"})
    .when("/bigdata", {templateUrl: "partials/bigdata-services.html", controller: "PageCtrl"})
    .when("/analytics", {templateUrl: "partials/analytics-services.html", controller: "PageCtrl"})
    .when("/marketing-analytics", {templateUrl: "partials/marketing-analytics.html", controller: "PageCtrl"})
    .when("/risk-analytics", {templateUrl: "partials/risk-analytics.html", controller: "PageCtrl"})
    .when("/reco-analytics", {templateUrl: "partials/reco-analytics.html", controller: "PageCtrl"})
    .when("/blogs", {templateUrl: "partials/blogs.html", controller: "PageCtrl"})
    .when("/docLayout", {templateUrl: "partials/docLayout.html", controller: ''})
    .when("/machine-learning", {templateUrl: "partials/machine-learning.html", controller: "PageCtrl"})
    .when("/apache-spark", {templateUrl: "partials/spark/apache-spark.html", controller: "PageCtrl"})
    .when("/login", {templateUrl: "partials/login.html", controller: "LoginCtrl"})
    .when("/signup", {templateUrl: "partials/signup.html", controller: 'SignupCtrl'})
    .when("/dashboard", {templateUrl: "partials/dashboard.html", controller: ''})

    .when("/hadoop", {templateUrl: "partials/hadoop.html", controller: ""})

    // Pages
    .when("/about", {templateUrl: "partials/about.html", controller: "PageCtrl"})
    .when("/faq", {templateUrl: "partials/faq.html", controller: "PageCtrl"})
    .when("/pricing", {templateUrl: "partials/pricing.html", controller: "PageCtrl"})
    .when("/services", {templateUrl: "partials/services.html", controller: "PageCtrl"})
    .when("/contact", {templateUrl: "partials/contact.html", controller: "ContactCtrl"})
    // Blog
    .when("/blog", {templateUrl: "partials/blog.html", controller: "BlogCtrl"})
    .when("/blog/post", {templateUrl: "partials/blog_item.html", controller: "BlogCtrl"})

    // else 404
    .otherwise("/404", {templateUrl: "partials/404.html", controller: "PageCtrl"});
}]);

  app.config(function ($httpProvider) {
    $httpProvider.interceptors.push(function ($rootScope, $q, $window, $location) {
      return {
        request: function(config) {
          if ($window.localStorage.token) {
            config.headers.Authorization = 'Bearer ' + $window.localStorage.token;
          }
          return config;
        },
        responseError: function(response) {
          if (response.status === 401 || response.status === 403) {
            $location.path('/login');
          }
          return $q.reject(response);
        }
      }
    });
  });
/**
 * Controls the Blog
 */



app.controller('BlogCtrl', function (/* $scope, $location, $http */) {
  console.log("Blog Controller reporting for duty.");
});

/**
 * Controls all other Pages
 */
app.controller('PageCtrl', function (/* $scope, $location, $http */) {


   // Activates the Carousel
  $('.carousel').carousel({
    interval: 5000
  });

  // Activates Tooltips for Social Links
  $('.tooltip-social').tooltip({
    selector: "a[data-toggle=tooltip]"
  })

});



app.controller('CarouselDemoCtrl', function($scope){
  $scope.myInterval = 3000;
 
  $scope.slides = [
    {
      image: 'images/bigdata-slider.jpg'

    },
    {
      image: 'images/data-slider.jpg',
      caption: 'Data Integration Services'
    },
    {
      image: 'images/analytics-slider.jpg'
    }
  ];
});

app.controller('hadoopScrollCtrl', function($scope, $location, $anchorScroll) {
  $scope.scrollTo = function(id) {
    $location.hash(id);
    console.log($location.hash());
    $anchorScroll();
  };
});