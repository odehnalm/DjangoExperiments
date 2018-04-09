var directiveModule = angular.module('angularjs-dropdown-multiselect', []);

directiveModule.directive('ngDropdownMultiselect', ['$filter', '$document', '$compile', '$parse', '$timeout',

function ($filter, $document, $compile, $parse, $timeout) {
    return {
        restrict: 'AE',
        scope: {
            selectedModel: '=',
            options: '=',
            extraSettings: '=',
            events: '=',
            searchFilter: '=?',
            translationTexts: '=',
            groupBy: '@'
        },
        template: function (element, attrs) {
            var checkboxes = attrs.checkboxes ? true : false;
            var groups = attrs.groupBy ? true : false;

            var template = '<div class="multiselect-parent btn-group dropdown-multiselect">';
            template += '<button type="button" class="dropdown-toggle " ng-class="settings.buttonClasses" ng-click="toggleDropdown()">{{getButtonText()}}&nbsp;<span class="caret"></span></button>';
            template += '<ul class="dropdown-menu dropdown-menu-form" ng-style="{display: open ? \'block\' : \'none\', height : settings.scrollable ? settings.scrollableHeight : \'auto\' }" style="overflow: scroll" >';
            
            template += '<li ng-show="settings.enableSearch"><div class="dropdown-header"><input type="text" class="form-control" style="width: 100%;" ng-model="searchFilter" placeholder="{{texts.searchPlaceholder}}" ng-keyup="deselectAll()" /></li>';
            template += '<li ng-show="settings.enableSearch" class="divider"></li>';
            
            template += '<li ng-hide="canShowSelectAll()"><a data-ng-click="selectAll()" ng-hide="(options.length > 0 && (options.length === selectedModel.length) || (filterData.length === selectedModel.length))"><span><input type="checkbox"></span>&nbsp;{{texts.checkAll}}</a>';
            template += '<a data-ng-click="deselectAll();" ng-show="(options.length > 0 && (options.length === selectedModel.length) || (filterData.length === selectedModel.length))"><span><input type="checkbox" checked></span>&nbsp;{{texts.checkAll}}</a></li>';
            template += '<li ng-hide="(!settings.showCheckAll || settings.selectionLimit > 0) && !settings.showUncheckAll" class="divider"></li>';           

            if (groups) {
                template += '<li ng-repeat-start="option in getDisplayList()" ng-show="getPropertyForObject(option, settings.groupBy) !== getPropertyForObject(getDisplayList()[$index - 1], settings.groupBy)" role="presentation" class="dropdown-header">{{ getGroupTitle(getPropertyForObject(option, settings.groupBy)) }}</li>';
                template += '<li ng-repeat-end role="presentation">';
            } else {
                template += '<li role="presentation" ng-repeat="option in getDisplayList()">';
            }

            template += '<a role="menuitem" tabindex="-1" ng-click="setSelectedItem(getPropertyForObject(option,settings.idProp))">';

            if (checkboxes) {
                template += '<div class="checkbox"><label><input class="checkboxInput" type="checkbox" ng-click="checkboxClick($event, getPropertyForObject(option,settings.idProp))" ng-checked="isChecked(getPropertyForObject(option,settings.idProp))" /> {{getPropertyForObject(option, settings.displayProp)}}</label></div></a>';
            } else {
                template += '<span data-ng-class="{\'glyphicon glyphicon-ok\': isChecked(getPropertyForObject(option,settings.idProp))}"></span> {{getPropertyForObject(option, settings.displayProp)}}</a>';
            }

            template += '</li>';

            template += '<li class="divider" ng-show="settings.selectionLimit > 1"></li>';
            template += '<li role="presentation" ng-show="settings.selectionLimit > 1"><a role="menuitem">{{selectedModel.length}} {{texts.selectionOf}} {{settings.selectionLimit}} {{texts.selectionCount}}</a></li>';

            template += '</ul>';
            template += '</div>';

            element.html(template);
        },
        link: function ($scope, $element, $attrs) {
            var $dropdownTrigger = $element.children()[0];

            $scope.toggleDropdown = function () {
                $scope.open = !$scope.open;
            };

            $scope.checkboxClick = function ($event, id) {
                $scope.setSelectedItem(id);
                $event.stopImmediatePropagation();
            };

            $scope.externalEvents = {
                onItemSelect: angular.noop,
                onItemDeselect: angular.noop,
                onSelectAll: angular.noop,
                onUnselectAll: angular.noop,
                onInitDone: angular.noop,
                onMaxSelectionReached: angular.noop
            };

            $scope.settings = {
                dynamicTitle: true,
                scrollable: true,
                scrollableHeight: '400px',
                closeOnBlur: true,
                displayProp: 'label',
                idProp: 'id',
                externalIdProp: 'id',
                enableSearch: false,
                selectionLimit: 0,
                showCheckAll: false,
                showUncheckAll: false,
                closeOnSelect: false,
                buttonClasses: 'customBtn btn-default',
                closeOnDeselect: false,
                groupBy: $attrs.groupBy || undefined,
                groupByTextProvider: null,
                smartButtonMaxItems: 0,
                smartButtonTextConverter: angular.noop
            };

            $scope.texts = {
                checkAll: 'Select All',
                uncheckAll: 'Deselect All',
                selectionCount: 'checked',
                selectionOf: '/',
                searchPlaceholder: 'Search...',
                buttonDefaultText: 'Select items',
                dynamicButtonTextSuffix: '    selected'
            };

            $scope.canShowSelectAll = function(){
            	return (!$scope.settings.showCheckAll || $scope.settings.selectionLimit > 0) && !$scope.settings.showUncheckAll;
            };
            
            $scope.searchFilter = $scope.searchFilter || '';
            var sortByFields = $attrs.groupBy ? [$attrs.groupBy, $scope.settings.displayProp]:[$scope.settings.displayProp];
            
            var numCellsToCreate = 50;
            var numCellsToCreateThreshold = 500;
            $scope.initInfiniteScroll = function() {
                $scope.scrollTop = 0;
                $scope.visibleDataProvider = angular.copy($scope.options);
                if($attrs.groupBy){
                	 _.sortBy( $scope.visibleDataProvider, $attrs.groupBy);
                }               
                var initCellsToCreate = $scope.visibleDataProvider.slice(0, 
                		($scope.visibleDataProvider.length > numCellsToCreateThreshold) ? numCellsToCreateThreshold : $scope.visibleDataProvider.length);
                if($attrs.groupBy){
                    $scope.orderedItems = $filter('orderBy')(initCellsToCreate, sortByFields); 
                }else {
                	$scope.unOrderedItems = initCellsToCreate;
                }
                $scope.marker = initCellsToCreate.length;
                if($scope.open){
                    $('.dropdown-menu', $element[0]).scrollTop(0);   
                }
                var onScrollThrottle = _.throttle($scope.onScroll, 49);
                $('.dropdown-menu', $element[0])[0].addEventListener('scroll', onScrollThrottle);
                $scope.updateDisplayList();
            };
            
            function initInfiniteScrollForFilteredData(filteredData) {
                $scope.filterDataProvider = angular.copy(filteredData);
                if($attrs.groupBy){
                	_.sortBy($scope.filterDataProvider, $attrs.groupBy);
                }   
                var initCellsToCreate = $scope.filterDataProvider.slice(0, 
                		($scope.filterDataProvider.length > numCellsToCreateThreshold) ? numCellsToCreateThreshold : $scope.filterDataProvider.length);
                if($attrs.groupBy){
                    $scope.filteredData = $filter('orderBy')(initCellsToCreate, sortByFields); 
                }else {
                	$scope.filteredData = initCellsToCreate;
                }
                $scope.filtermarker = initCellsToCreate.length;
                $scope.$apply();                
            };
            
            
            $scope.getDisplayList = function(){
                if(isFilterActive()){
                    return $scope.filteredData;
                }else{
                    if(isOrderedList()){
                        return $scope.orderedItems;
                    }else{
                        return $scope.unOrderedItems;
                    }                       
                }
            };
            
            function isFilterActive(){
                return $scope.searchFilter && $scope.searchFilter.trim() !== '';                    
            }
            
            function isOrderedList(){
              return ($attrs.groupBy &&  $scope.orderedItems &&  $scope.orderedItems.length);
            }
            
            function onFilterChange(newValue, oldValue){
                if(newValue !== oldValue){
                    console.log("searchFilter : newValue : "+ newValue);
                    if(newValue === ''){
                      return ;                      
                    } 
                var _filtered;
            	if(angular.isObject($scope.options[0])){
            		var searchExpression = {};
            		searchExpression[$scope.settings.displayProp] = newValue;
            		_filtered = $filter('filter')($scope.options,  searchExpression);            		
            	}else{
            		_filtered = $filter('filter')($scope.options, newValue);
            	}
            	initInfiniteScrollForFilteredData(_filtered);
                }                
            }
            
            var onFilterChangeDebounced = _.debounce(onFilterChange, 300);
            
            $scope.$watch('searchFilter', function (newValue, oldValue) {
                onFilterChangeDebounced(newValue, oldValue);
            });
            
            $scope.updateFilteredDataDisplayList = function() {
                  if ($scope.filtermarker !== $scope.filterDataProvider.length) {
                    var newCells = $scope.filterDataProvider.slice($scope.filtermarker, $scope.filtermarker + numCellsToCreate);                	
                    var lastIndexOf = function(group){
                        return _.lastIndexOf(_.map($scope.filteredData, function (item) {
                          return item[$attrs.groupBy];
                        }),  group);
                    };
                    if(!isOrderedList()){
                      angular.forEach(newCells, function(item) {
                         $scope.filteredData.push(item);
                      });
                    }else{
                      angular.forEach(newCells, function(item) {
                          var lastIdx = lastIndexOf(item[$attrs.groupBy]);
                          if(lastIdx === -1){
                              $scope.filteredData.push(item);
                          }else{
                              $scope.filteredData.splice(lastIdx + 1, 0, item );   
                          }
                      });
                    }
                    $scope.filtermarker = $scope.filteredData.length;
                    console.log("Number of filter records loaded : " + $scope.filtermarker);
                }
            };
            $scope.updateDisplayList = function() {
                if ($scope.marker !== $scope.visibleDataProvider.length) {
                    var newCells = $scope.visibleDataProvider.slice($scope.marker, $scope.marker + numCellsToCreate);                	
                	
                    var lastIndexOf = function(group){
                        return _.lastIndexOf(_.map($scope.orderedItems, function (item) {
                          return item[$attrs.groupBy];
                        }),  group);
                    }
                    
                    if(isOrderedList()){
                        angular.forEach(newCells, function(item) {
                            var lastIdx = lastIndexOf(item[$attrs.groupBy]);
                            if(lastIdx === -1){
                               $scope.orderedItems.push(item);
                            }else{
                               $scope.orderedItems.splice(lastIdx + 1, 0, item );   
                            }
                        });
                         $scope.marker = $scope.orderedItems.length;
                    }else{
                        angular.forEach(newCells, function(item) {
                            $scope.unOrderedItems.push(item);
                        });
                        $scope.marker = $scope.unOrderedItems.length;
                    }

                        console.log("Number of records loaded : " + $scope.marker);
                }
            };

            $scope.onScroll = function(evt) {
                var currentScrollTop = $('.dropdown-menu', $element[0]).prop('scrollTop');
                if (currentScrollTop > $scope.scrollTop) {
                    $scope.scrollTop = currentScrollTop;
                    if(isFilterActive()){
                       $scope.updateFilteredDataDisplayList();
                    }else{
                       $scope.updateDisplayList();
                    }  
                    $timeout(function(){
                    	$scope.$apply();                    	
                    }, 1);                                        
                }
            };

            $scope.$watch('options', function (newValue) {
                 if (angular.isDefined(newValue) && newValue.length) {
                   $scope.searchFilter = '';
                   if (newValue.length > numCellsToCreateThreshold) {
                       $scope.initInfiniteScroll();
                   }else if (angular.isDefined($scope.settings.groupBy)) {
                       $scope.orderedItems = $filter('orderBy')(newValue, sortByFields); 
                   }else{
                      $scope.unOrderedItems = newValue;
                   }  
                }
             });

            angular.extend($scope.settings, $scope.extraSettings || []);
            angular.extend($scope.externalEvents, $scope.events || []);
            angular.extend($scope.texts, $scope.translationTexts);

            $scope.singleSelection = $scope.settings.selectionLimit === 1;
            function getFindObj(id) {
                var findObj = {};

                if ($scope.settings.externalIdProp === '') {
                    findObj[$scope.settings.idProp] = id;
                } else {
                    findObj[$scope.settings.externalIdProp] = id;
                }

                return findObj;
            }

            function clearObject(object) {
                for (var prop in object) {
                    delete object[prop];
                }
            }

            if ($scope.singleSelection) {
                if (angular.isArray($scope.selectedModel) && $scope.selectedModel.length === 0) {
                    clearObject($scope.selectedModel);
                }
            }

            if ($scope.settings.closeOnBlur) {            	
                $document.on('click', function (e) {
                	if(!$scope.open){
                		return;
                	} 
                    var target = e.target.parentElement;
                    var parentFound = false;

                    while (angular.isDefined(target) && target !== null && !parentFound) {
                        if (_.contains(target.className.split(' '), 'multiselect-parent') && !parentFound) {
                            if (target === $dropdownTrigger) {
                                parentFound = true;
                            }
                        }
                        target = target.parentElement;
                    }

                    if (!parentFound) {
                        $scope.$apply(function () {
                            $scope.open = false;
                        });
                    }
                });
            }

            $scope.getGroupTitle = function (groupValue) {
                if ($scope.settings.groupByTextProvider !== null) {
                    return $scope.settings.groupByTextProvider(groupValue);
                }

                return groupValue;
            };

            $scope.getButtonText = function () {
                if ($scope.settings.dynamicTitle && ($scope.selectedModel && $scope.selectedModel.length > 0 || (angular.isObject($scope.selectedModel) && _.keys($scope.selectedModel).length > 0))) {
                    if ($scope.settings.smartButtonMaxItems > 0) {
                        var itemsText = [];

                        angular.forEach($scope.options, function (optionItem) {
                            if ($scope.isChecked($scope.getPropertyForObject(optionItem, $scope.settings.idProp))) {
                                var displayText = $scope.getPropertyForObject(optionItem, $scope.settings.displayProp);
                                var converterResponse = $scope.settings.smartButtonTextConverter(displayText, optionItem);

                                itemsText.push(converterResponse ? converterResponse : displayText);
                            }
                        });

                        if ($scope.selectedModel.length > $scope.settings.smartButtonMaxItems) {
                            itemsText = itemsText.slice(0, $scope.settings.smartButtonMaxItems);
                            itemsText.push('...');
                        }

                        return itemsText.join(', ');
                    } else {
                        var totalSelected;

                        if ($scope.singleSelection) {
                            totalSelected = ($scope.selectedModel !== null && angular.isDefined($scope.selectedModel[$scope.settings.idProp])) ? 1 : 0;
                        } else {
                            totalSelected = angular.isDefined($scope.selectedModel) ? $scope.selectedModel.length : 0;
                        }

                        if (totalSelected === 0) {
                            return $scope.texts.buttonDefaultText;
                        } else {
                            return totalSelected + ' ' + $scope.texts.dynamicButtonTextSuffix;
                        }
                    }
                } else {
                    return $scope.texts.buttonDefaultText;
                }
            };

            $scope.getPropertyForObject = function (object, property) {
                if (angular.isDefined(object) && object.hasOwnProperty(property)) {
                    return object[property];
                }

                return '';
            };
            
     
            $scope.selectAll = function () { 
            	$scope.deselectAll(false);
               
            	if(angular.isObject($scope.options[0])){
            		var searchExpression = {};
            		searchExpression[$scope.settings.displayProp] = $scope.searchFilter;
            		$scope.filterData = $filter('filter')($scope.options,  searchExpression);           		
            	}else{
            		$scope.filterData = $filter('filter')($scope.options, $scope.searchFilter);
            	} 
            	                
                angular.forEach($scope.filterData, function (value) {                	
                    $scope.setSelectedItem(value[$scope.settings.idProp], true);
                }); 
                
                $scope.externalEvents.onSelectAll();
                
            };

            $scope.deselectAll = function (sendEvent) {
              

                if ($scope.singleSelection) {
                    clearObject($scope.selectedModel);
                } else {
                    $scope.selectedModel.splice(0, $scope.selectedModel.length);
                }
                sendEvent = sendEvent || true;
                if (sendEvent) {
                    $scope.externalEvents.onUnselectAll();
                }
            };

            $scope.setSelectedItem = function (id, dontRemove) {
                var findObj = getFindObj(id);
                var finalObj = null;

                if ($scope.settings.externalIdProp === '') {
                    finalObj = _.find($scope.options, findObj);
                } else {
                    finalObj = findObj;
                }

                if ($scope.singleSelection) {
                    clearObject($scope.selectedModel);
                    angular.extend($scope.selectedModel, finalObj);
                    $scope.externalEvents.onItemSelect(finalObj);
                    if ($scope.settings.closeOnSelect) $scope.open = false;

                    return;
                }

                dontRemove = dontRemove || false;

                var exists = _.findIndex($scope.selectedModel, findObj) !== -1;

                if (!dontRemove && exists) {
                    $scope.selectedModel.splice(_.findIndex($scope.selectedModel, findObj), 1);
                    $scope.externalEvents.onItemDeselect(findObj);
                } else if (!exists && ($scope.settings.selectionLimit === 0 || $scope.selectedModel.length < $scope.settings.selectionLimit)) {
                    $scope.selectedModel.push(finalObj);
                    $scope.externalEvents.onItemSelect(finalObj);
                }
                if ($scope.settings.closeOnSelect) $scope.open = false;
            };

            $scope.isChecked = function (id) {
                if ($scope.singleSelection) {
                    return $scope.selectedModel !== null && angular.isDefined($scope.selectedModel[$scope.settings.idProp]) && $scope.selectedModel[$scope.settings.idProp] === getFindObj(id)[$scope.settings.idProp];
                }

                return _.findIndex($scope.selectedModel, getFindObj(id)) !== -1;
            };

            $scope.externalEvents.onInitDone();
        }
    };
}]);


