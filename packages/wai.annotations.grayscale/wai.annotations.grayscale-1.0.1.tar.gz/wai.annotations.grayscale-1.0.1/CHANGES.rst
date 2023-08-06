Changelog
=========

1.0.1 (2022-06-13)
------------------

- `FromGrayscale` class now uses `numpy.frombuffer` instead of deprecated `numpy.fromstring` method.
- `FromGrayscale` class now outputs logging message if setting of new annotation indices fails, as error
  occurs before the `wai.annotations - Sourced ...` logging message, making it possible to track the image
  causing the problem.

1.0.0 (2022-05-31)
------------------

- Initial release.

