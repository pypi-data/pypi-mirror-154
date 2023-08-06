"use strict";

suite('rb/views/ScreenshotThumbnail', function () {
  var model;
  var view;
  beforeEach(function () {
    model = new RB.Screenshot();
    model.url = '/screenshots/123/';
    model.id = 123;
    model.attributes.id = 123;
    model.set('loaded', true);
    var template = '<div><a class="edit"></a><a class="delete">X</a></div>';
    view = new RB.ScreenshotThumbnail({
      el: $(template).appendTo($testsScratch),
      model: model
    });
    view.render();
    spyOn(model, 'trigger').and.callThrough();
    spyOn(view, 'trigger').and.callThrough();
  });
  describe('Actions', function () {
    it('Begin caption editing', function () {
      view.$caption.inlineEditor('startEdit');
      expect(view.trigger).toHaveBeenCalledWith('beginEdit');
    });
    it('Cancel caption editing', function () {
      view.$caption.inlineEditor('startEdit');
      expect(view.trigger).toHaveBeenCalledWith('beginEdit');
      view.$caption.inlineEditor('cancel');
      expect(view.trigger).toHaveBeenCalledWith('endEdit');
    });
    it('Save caption', function () {
      spyOn(model, 'save');
      view.$caption.inlineEditor('startEdit');
      expect(view.trigger).toHaveBeenCalledWith('beginEdit');
      view.$el.find('input').val('Foo').triggerHandler('keyup');
      view.$caption.inlineEditor('submit');
      expect(view.trigger).toHaveBeenCalledWith('endEdit');
      expect(model.get('caption')).toBe('Foo');
      expect(model.save).toHaveBeenCalled();
    });
    it('Delete', function () {
      spyOn(model, 'destroy').and.callThrough();
      spyOn($, 'ajax').and.callFake(function (options) {
        return options.success();
      });
      spyOn(view.$el, 'fadeOut').and.callFake(function (done) {
        return done();
      });
      spyOn(view, 'remove');
      view.$el.find('a.delete').click();
      expect($.ajax).toHaveBeenCalled();
      expect(model.destroy).toHaveBeenCalled();
      expect(model.trigger.calls.argsFor(0)[0]).toBe('destroying');
      expect(view.$el.fadeOut).toHaveBeenCalled();
      expect(view.remove).toHaveBeenCalled();
    });
  });
});

//# sourceMappingURL=screenshotThumbnailViewTests.js.map