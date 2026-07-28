---
title: Prototype Pollution Prevention Cheat Sheet¶
source: cheatsheetseries.owasp.org
url: https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html
collector: owasp
category: web-security
tags:
- web-security
- prototype
- pollution
- object
- prevention
date_collected: '2026-07-26T12:36:48.254167Z'
language: unknown
---

# Prototype Pollution Prevention Cheat Sheet[¶](#prototype-pollution-prevention-cheat-sheet)

## Explanation[¶](#explanation)

Prototype Pollution is a critical vulnerability that can allow attackers to manipulate an application's JavaScript objects and properties, leading to serious security issues such as unauthorized access to data, privilege escalation, and even remote code execution.

For examples of why this is dangerous, see the links in the [Other resources](#other-resources) section below.

## Suggested protection mechanisms[¶](#suggested-protection-mechanisms)

### Use "new Set()" or "new Map()"[¶](#use-new-set-or-new-map)

Developers should use
```
new Set()
```

or
```
new Map()
```

instead of using object literals:
```
```
let allowedTags = new Set();
allowedTags.add('b');
if(allowedTags.has('b')){
  //...
}

let options = new Map();
options.set('spaces', 1);
let spaces = options.get('spaces')```
```

### If objects or object literals are required[¶](#if-objects-or-object-literals-are-required)

If objects have to be used then they should be created using the
```
Object.create(null)
```

API to ensure they don't inherit from the Object prototype:
```
```
let obj = Object.create(null);```
```

If object literals are required then as a last resort you could use the
```
__proto__
```

property:
```
```
let obj = {__proto__:null};```
```

### Use object "freeze" and "seal" mechanisms[¶](#use-object-freeze-and-seal-mechanisms)

You can also use the
```
Object.freeze()
```

and
```
Object.seal()
```

APIs to prevent built-in prototypes from being modified however this can break the application if the libraries they use modify the built-in prototypes.

### Node.js configuration flag[¶](#nodejs-configuration-flag)

Node.js also offers the ability to remove the
```
__proto__
```

property completely using the
```
--disable-proto=delete
```

flag. Note this is a defense in depth measure.

Prototype pollution is still possible using
```
constructor.prototype
```

properties but removing
```
__proto__
```

helps reduce attack surface and prevent certain attacks.

### Other resources[¶](#other-resources)

### Credits[¶](#credits)

Credit to [Gareth Hayes](https://garethheyes.co.uk/) for providing the original protection guidance [in this comment](https://github.com/OWASP/ASVS/issues/1563#issuecomment-1470027723).
