# Contributing to TorPaste

Thanks for your interest in TorPaste! Here are a few instructions and tips to get you started.

## Setting up your environment

The [README](https://github.com/DaKnOb/TorPaste/blob/master/README.md) should contain enough information regarding how you can install and run TorPaste. It's just a matter of using either pip directly to install a few Python packages, or using Docker so that all that is done automatically.

TorPaste currently runs on Python 2.7, although full Python 3 compatibility is coming very soon.

## Contribution guidelines

### Everyone is welcome!

TorPaste is a small project, but there is a lot to do before it has all the features that its inspiration, Pastebin, has. Everyone is welcome to lend a hand! 

If you see small improvements you can do, go ahead and submit a pull request.

If you have an idea for a more significant improvement, such as a new feature, please create [a GitHub issue](https://github.com/DaKnOb/TorPaste/issues) first, so that we can keep track of what's going on. Naturally, don't forget to check existing issues first!

### Conventions

Fork the repo and make your changes in a branch with a clear and self-explanatory name.

Update the documentation within the code when creating or modifying features. Try to keep it clear and concise.

We use [PEP8](https://www.python.org/dev/peps/pep-0008/) as coding style convention. There's probably no need to read the whole thing, though: just make sure your code looks like what's already there.

### Testing

Before creating a merge request, please test TorPaste. A unit test suite is under development, but in the meantime, make sure the following things still work when your work is done:

- running TorPaste from the command line: `pip install -r requirements.txt; python torpaste.py` works;
- running TorPaste from Docker: `docker build daknob/torpaste . ; docker run -d -p 5000:80 daknob/torpaste` works, and afterwards, `docker ps` shows the container active;
- in both cases above, TorPaste is accessible at localhost:5000;
- in both cases, you can create a new paste, even with UTF-8 characters (here's one that you can copy/paste: ✔);
- in both cases, pastes' metadata is displayed and correct (✔ counts as three bytes!);
- in both cases, you can open the paste list and the "About" page by using the links in the navigation bar.


### Community guidelines

Just be nice with everyone!
