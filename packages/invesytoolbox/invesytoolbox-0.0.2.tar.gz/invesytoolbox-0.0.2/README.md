# invesytoolbox

A set of useful tools, created for my own convenience, but you might find it useful too.

Why "invesy"? Invesy (from German **In**halts**ve**rwaltungs**sy**stem == content management system) is a closed source cms I created with Thomas Macher. It's only used in-house, that's why we didn't bother making it open source.

Invesy runs on Zope, so most of the individual website's logic runs in restricted Python. That's one reason for this toolbox: providing a set of useful functions in one single package which can be allowed in our restricted Python environment.

That's also why all date and time functions also take into account the old DateTime (as opposed to datetime) package, which is Zope is still relying upon heavily.

Lastly there are a few functions I need for Python scripts on my servers (which run FreeBSD, but they should run on any Unixoid system, possibly even Windows).
