angular.module('tutorialWebApp')
  .controller('ContactCtrl', function($scope, Auth) {
    $scope.contactus = function() {
      Auth.contactus({
        name: $scope.displayName,
        number:$scope.phoneNumber,
        email: $scope.email,
        comment:$scope.comment
      });
    };
    $scope.pageClass = 'fadeZoom'
  });
