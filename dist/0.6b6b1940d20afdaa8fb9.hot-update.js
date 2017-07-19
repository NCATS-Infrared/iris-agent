webpackHotUpdate(0,{

/***/ 490:
/***/ (function(module, exports, __webpack_require__) {

	eval("'use strict';\n\nObject.defineProperty(exports, \"__esModule\", {\n  value: true\n});\n\nvar _react = __webpack_require__(2);\n\nvar _react2 = _interopRequireDefault(_react);\n\nvar _reactRedux = __webpack_require__(30);\n\nvar _index = __webpack_require__(43);\n\nfunction _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }\n\n// References to arg components, indexed by id (position of arg in list)\nvar arg_name = {},\n    arg_type = {},\n    arg_string = {};\n\n// Update arg state using reference to components\nvar onChangeInput = function onChangeInput(dispatch, id) {\n  var new_values = {\n    arg_name: arg_name[id].value,\n    arg_type: arg_type[id].value,\n    arg_string: arg_string[id].value\n  };\n  dispatch((0, _index.updateCommandArg)(id, new_values));\n};\n\nvar onClickDelete = function onClickDelete(dispatch, id) {\n  console.log(\"delete \" + id);\n  dispatch((0, _index.deleteCommandArg)(id));\n};\n\nvar ArgumentAnnotation = function ArgumentAnnotation(_ref) {\n  var dispatch = _ref.dispatch,\n      id = _ref.id,\n      name = _ref.name,\n      string = _ref.string,\n      arg_t = _ref.arg_t;\n  return _react2.default.createElement(\n    'div',\n    { className: 'arg_annotation' },\n    _react2.default.createElement('input', { type: 'text', className: 'arg_name', placeholder: 'name of arg', onChange: function onChange() {\n        return onChangeInput(dispatch, id);\n      }, ref: function ref(node) {\n        arg_name[id] = node;\n      }, value: name }),\n    _react2.default.createElement(\n      'select',\n      { className: 'arg_type', value: arg_t, onChange: function onChange() {\n          return onChangeInput(dispatch, id);\n        }, ref: function ref(node) {\n          arg_type[id] = node;\n        } },\n      _react2.default.createElement(\n        'option',\n        null,\n        'Int'\n      ),\n      _react2.default.createElement(\n        'option',\n        null,\n        'String'\n      ),\n      _react2.default.createElement(\n        'option',\n        null,\n        'Array'\n      ),\n      _react2.default.createElement(\n        'option',\n        null,\n        'Float'\n      ),\n      _react2.default.createElement(\n        'option',\n        null,\n        'Any'\n      ),\n      _react2.default.createElement(\n        'option',\n        null,\n        'Dataframe'\n      )\n    ),\n    _react2.default.createElement('input', { type: 'text', className: 'arg_string', placeholder: 'Message to request this argument from user...', onChange: function onChange() {\n        return onChangeInput(dispatch, id);\n      }, ref: function ref(node) {\n        arg_string[id] = node;\n      }, value: string }),\n    _react2.default.createElement(\n      'button',\n      { onClick: function onClick() {\n          return onClickDelete(dispatch, id);\n        } },\n      'Delete'\n    )\n  );\n};\n\nvar mapStateToProps = function mapStateToProps(state) {\n  return {};\n};\n\nArgumentAnnotation = (0, _reactRedux.connect)(mapStateToProps)(ArgumentAnnotation);\n\nexports.default = ArgumentAnnotation;//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vLi9hcHAvY29tcG9uZW50cy9Bcmd1bWVudEFubm90YXRpb24uanM/MzM3NCJdLCJuYW1lcyI6WyJhcmdfbmFtZSIsImFyZ190eXBlIiwiYXJnX3N0cmluZyIsIm9uQ2hhbmdlSW5wdXQiLCJkaXNwYXRjaCIsImlkIiwibmV3X3ZhbHVlcyIsInZhbHVlIiwib25DbGlja0RlbGV0ZSIsImNvbnNvbGUiLCJsb2ciLCJBcmd1bWVudEFubm90YXRpb24iLCJuYW1lIiwic3RyaW5nIiwiYXJnX3QiLCJub2RlIiwibWFwU3RhdGVUb1Byb3BzIiwic3RhdGUiXSwibWFwcGluZ3MiOiI7Ozs7OztBQUFBOzs7O0FBQ0E7O0FBQ0E7Ozs7QUFFQTtBQUNBLElBQUlBLFdBQVcsRUFBZjtBQUFBLElBQW1CQyxXQUFXLEVBQTlCO0FBQUEsSUFBa0NDLGFBQWEsRUFBL0M7O0FBRUE7QUFDQSxJQUFNQyxnQkFBZ0IsU0FBaEJBLGFBQWdCLENBQUNDLFFBQUQsRUFBV0MsRUFBWCxFQUFrQjtBQUN0QyxNQUFNQyxhQUFhO0FBQ2pCTixjQUFVQSxTQUFTSyxFQUFULEVBQWFFLEtBRE47QUFFakJOLGNBQVVBLFNBQVNJLEVBQVQsRUFBYUUsS0FGTjtBQUdqQkwsZ0JBQVlBLFdBQVdHLEVBQVgsRUFBZUU7QUFIVixHQUFuQjtBQUtBSCxXQUFTLDZCQUFpQkMsRUFBakIsRUFBcUJDLFVBQXJCLENBQVQ7QUFDRCxDQVBEOztBQVNBLElBQU1FLGdCQUFnQixTQUFoQkEsYUFBZ0IsQ0FBQ0osUUFBRCxFQUFXQyxFQUFYLEVBQWtCO0FBQ3RDSSxVQUFRQyxHQUFSLENBQVksWUFBVUwsRUFBdEI7QUFDQUQsV0FBUyw2QkFBaUJDLEVBQWpCLENBQVQ7QUFDRCxDQUhEOztBQUtBLElBQUlNLHFCQUFxQjtBQUFBLE1BQUdQLFFBQUgsUUFBR0EsUUFBSDtBQUFBLE1BQWFDLEVBQWIsUUFBYUEsRUFBYjtBQUFBLE1BQWlCTyxJQUFqQixRQUFpQkEsSUFBakI7QUFBQSxNQUF1QkMsTUFBdkIsUUFBdUJBLE1BQXZCO0FBQUEsTUFBK0JDLEtBQS9CLFFBQStCQSxLQUEvQjtBQUFBLFNBQ3JCO0FBQUE7QUFBQSxNQUFLLFdBQVUsZ0JBQWY7QUFDSSw2Q0FBTyxNQUFLLE1BQVosRUFBbUIsV0FBVSxVQUE3QixFQUF3QyxhQUFZLGFBQXBELEVBQWtFLFVBQVU7QUFBQSxlQUFNWCxjQUFjQyxRQUFkLEVBQXdCQyxFQUF4QixDQUFOO0FBQUEsT0FBNUUsRUFBK0csS0FBSyxtQkFBUTtBQUFDTCxpQkFBU0ssRUFBVCxJQUFlVSxJQUFmO0FBQXFCLE9BQWxKLEVBQW9KLE9BQU9ILElBQTNKLEdBREo7QUFFSTtBQUFBO0FBQUEsUUFBUSxXQUFVLFVBQWxCLEVBQTZCLE9BQU9FLEtBQXBDLEVBQTJDLFVBQVU7QUFBQSxpQkFBTVgsY0FBY0MsUUFBZCxFQUF3QkMsRUFBeEIsQ0FBTjtBQUFBLFNBQXJELEVBQXdGLEtBQUssbUJBQVE7QUFBQ0osbUJBQVNJLEVBQVQsSUFBZVUsSUFBZjtBQUFxQixTQUEzSDtBQUNFO0FBQUE7QUFBQTtBQUFBO0FBQUEsT0FERjtBQUVFO0FBQUE7QUFBQTtBQUFBO0FBQUEsT0FGRjtBQUdFO0FBQUE7QUFBQTtBQUFBO0FBQUEsT0FIRjtBQUlFO0FBQUE7QUFBQTtBQUFBO0FBQUEsT0FKRjtBQUtFO0FBQUE7QUFBQTtBQUFBO0FBQUEsT0FMRjtBQU1FO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFORixLQUZKO0FBVUksNkNBQU8sTUFBSyxNQUFaLEVBQW1CLFdBQVUsWUFBN0IsRUFBMEMsYUFBWSwrQ0FBdEQsRUFBc0csVUFBVTtBQUFBLGVBQU1aLGNBQWNDLFFBQWQsRUFBd0JDLEVBQXhCLENBQU47QUFBQSxPQUFoSCxFQUFtSixLQUFLLG1CQUFRO0FBQUNILG1CQUFXRyxFQUFYLElBQWlCVSxJQUFqQjtBQUF1QixPQUF4TCxFQUEwTCxPQUFPRixNQUFqTSxHQVZKO0FBV0k7QUFBQTtBQUFBLFFBQVEsU0FBUztBQUFBLGlCQUFNTCxjQUFjSixRQUFkLEVBQXdCQyxFQUF4QixDQUFOO0FBQUEsU0FBakI7QUFBQTtBQUFBO0FBWEosR0FEcUI7QUFBQSxDQUF6Qjs7QUFlQSxJQUFNVyxrQkFBa0IsU0FBbEJBLGVBQWtCLENBQUNDLEtBQUQ7QUFBQSxTQUFZLEVBQVo7QUFBQSxDQUF4Qjs7QUFFQU4scUJBQXFCLHlCQUFRSyxlQUFSLEVBQXlCTCxrQkFBekIsQ0FBckI7O2tCQUVlQSxrQiIsImZpbGUiOiI0OTAuanMiLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHsgY29ubmVjdCB9IGZyb20gJ3JlYWN0LXJlZHV4JztcbmltcG9ydCB7IHVwZGF0ZUNvbW1hbmRBcmcsIGRlbGV0ZUNvbW1hbmRBcmcgfSBmcm9tICcuLi9hY3Rpb25zL2luZGV4LmpzJztcblxuLy8gUmVmZXJlbmNlcyB0byBhcmcgY29tcG9uZW50cywgaW5kZXhlZCBieSBpZCAocG9zaXRpb24gb2YgYXJnIGluIGxpc3QpXG5sZXQgYXJnX25hbWUgPSB7fSwgYXJnX3R5cGUgPSB7fSwgYXJnX3N0cmluZyA9IHt9O1xuXG4vLyBVcGRhdGUgYXJnIHN0YXRlIHVzaW5nIHJlZmVyZW5jZSB0byBjb21wb25lbnRzXG5jb25zdCBvbkNoYW5nZUlucHV0ID0gKGRpc3BhdGNoLCBpZCkgPT4ge1xuICBjb25zdCBuZXdfdmFsdWVzID0ge1xuICAgIGFyZ19uYW1lOiBhcmdfbmFtZVtpZF0udmFsdWUsXG4gICAgYXJnX3R5cGU6IGFyZ190eXBlW2lkXS52YWx1ZSxcbiAgICBhcmdfc3RyaW5nOiBhcmdfc3RyaW5nW2lkXS52YWx1ZVxuICB9O1xuICBkaXNwYXRjaCh1cGRhdGVDb21tYW5kQXJnKGlkLCBuZXdfdmFsdWVzKSk7XG59O1xuXG5jb25zdCBvbkNsaWNrRGVsZXRlID0gKGRpc3BhdGNoLCBpZCkgPT4ge1xuICBjb25zb2xlLmxvZyhcImRlbGV0ZSBcIitpZCk7XG4gIGRpc3BhdGNoKGRlbGV0ZUNvbW1hbmRBcmcoaWQpKTtcbn07XG5cbmxldCBBcmd1bWVudEFubm90YXRpb24gPSAoeyBkaXNwYXRjaCwgaWQsIG5hbWUsIHN0cmluZywgYXJnX3QgfSkgPT5cbiAgICA8ZGl2IGNsYXNzTmFtZT1cImFyZ19hbm5vdGF0aW9uXCI+XG4gICAgICAgIDxpbnB1dCB0eXBlPVwidGV4dFwiIGNsYXNzTmFtZT1cImFyZ19uYW1lXCIgcGxhY2Vob2xkZXI9XCJuYW1lIG9mIGFyZ1wiIG9uQ2hhbmdlPXsoKSA9PiBvbkNoYW5nZUlucHV0KGRpc3BhdGNoLCBpZCl9IHJlZj17bm9kZSA9PiB7YXJnX25hbWVbaWRdID0gbm9kZTt9fSB2YWx1ZT17bmFtZX0vPlxuICAgICAgICA8c2VsZWN0IGNsYXNzTmFtZT1cImFyZ190eXBlXCIgdmFsdWU9e2FyZ190fSBvbkNoYW5nZT17KCkgPT4gb25DaGFuZ2VJbnB1dChkaXNwYXRjaCwgaWQpfSByZWY9e25vZGUgPT4ge2FyZ190eXBlW2lkXSA9IG5vZGU7fX0+XG4gICAgICAgICAgPG9wdGlvbj5JbnQ8L29wdGlvbj5cbiAgICAgICAgICA8b3B0aW9uPlN0cmluZzwvb3B0aW9uPlxuICAgICAgICAgIDxvcHRpb24+QXJyYXk8L29wdGlvbj5cbiAgICAgICAgICA8b3B0aW9uPkZsb2F0PC9vcHRpb24+XG4gICAgICAgICAgPG9wdGlvbj5Bbnk8L29wdGlvbj5cbiAgICAgICAgICA8b3B0aW9uPkRhdGFmcmFtZTwvb3B0aW9uPlxuICAgICAgICA8L3NlbGVjdD5cbiAgICAgICAgPGlucHV0IHR5cGU9XCJ0ZXh0XCIgY2xhc3NOYW1lPVwiYXJnX3N0cmluZ1wiIHBsYWNlaG9sZGVyPVwiTWVzc2FnZSB0byByZXF1ZXN0IHRoaXMgYXJndW1lbnQgZnJvbSB1c2VyLi4uXCIgb25DaGFuZ2U9eygpID0+IG9uQ2hhbmdlSW5wdXQoZGlzcGF0Y2gsIGlkKX0gcmVmPXtub2RlID0+IHthcmdfc3RyaW5nW2lkXSA9IG5vZGU7fX0gdmFsdWU9e3N0cmluZ30vPlxuICAgICAgICA8YnV0dG9uIG9uQ2xpY2s9eygpID0+IG9uQ2xpY2tEZWxldGUoZGlzcGF0Y2gsIGlkKX0+RGVsZXRlPC9idXR0b24+XG4gICAgPC9kaXY+O1xuXG5jb25zdCBtYXBTdGF0ZVRvUHJvcHMgPSAoc3RhdGUpID0+ICh7fSk7XG5cbkFyZ3VtZW50QW5ub3RhdGlvbiA9IGNvbm5lY3QobWFwU3RhdGVUb1Byb3BzKShBcmd1bWVudEFubm90YXRpb24pO1xuXG5leHBvcnQgZGVmYXVsdCBBcmd1bWVudEFubm90YXRpb247XG5cblxuXG4vLyBXRUJQQUNLIEZPT1RFUiAvL1xuLy8gLi9hcHAvY29tcG9uZW50cy9Bcmd1bWVudEFubm90YXRpb24uanMiXSwic291cmNlUm9vdCI6IiJ9");

/***/ })

})