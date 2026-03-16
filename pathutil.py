#!/usr/bin/env python3
"""pathutil - File path manipulation utility."""
import os, argparse, sys, glob as globmod

def main():
    p = argparse.ArgumentParser(description='Path manipulation utility')
    sub = p.add_subparsers(dest='cmd')
    
    for name, help_text in [
        ('dirname', 'Get directory name'), ('basename', 'Get base name'),
        ('ext', 'Get extension'), ('stem', 'Get name without extension'),
        ('abs', 'Get absolute path'), ('real', 'Get real path (resolve symlinks)'),
        ('rel', 'Get relative path'), ('join', 'Join path components'),
        ('split', 'Split path into parts'), ('expand', 'Expand ~ and vars'),
        ('glob', 'Glob pattern match'), ('exists', 'Check if path exists'),
        ('common', 'Find common prefix'), ('rename', 'Batch rename preview'),
    ]:
        s = sub.add_parser(name, help=help_text)
        if name in ('dirname','basename','ext','stem','abs','real','expand','exists'):
            s.add_argument('path', nargs='+')
        elif name == 'rel':
            s.add_argument('path'); s.add_argument('--from', dest='start', default='.')
        elif name == 'join':
            s.add_argument('parts', nargs='+')
        elif name == 'split':
            s.add_argument('path')
        elif name == 'glob':
            s.add_argument('pattern')
        elif name == 'common':
            s.add_argument('paths', nargs='+')
        elif name == 'rename':
            s.add_argument('pattern'); s.add_argument('replacement')
            s.add_argument('files', nargs='+')
    
    args = p.parse_args()
    if not args.cmd: p.print_help(); return
    
    if args.cmd == 'dirname':
        for path in args.path: print(os.path.dirname(path))
    elif args.cmd == 'basename':
        for path in args.path: print(os.path.basename(path))
    elif args.cmd == 'ext':
        for path in args.path: print(os.path.splitext(path)[1])
    elif args.cmd == 'stem':
        for path in args.path: print(os.path.splitext(os.path.basename(path))[0])
    elif args.cmd == 'abs':
        for path in args.path: print(os.path.abspath(path))
    elif args.cmd == 'real':
        for path in args.path: print(os.path.realpath(path))
    elif args.cmd == 'rel':
        print(os.path.relpath(args.path, args.start))
    elif args.cmd == 'join':
        print(os.path.join(*args.parts))
    elif args.cmd == 'split':
        parts = []
        p_remaining = args.path
        while True:
            head, tail = os.path.split(p_remaining)
            if tail: parts.append(tail)
            elif head: parts.append(head); break
            else: break
            p_remaining = head
        for part in reversed(parts): print(part)
    elif args.cmd == 'expand':
        for path in args.path: print(os.path.expandvars(os.path.expanduser(path)))
    elif args.cmd == 'glob':
        for path in sorted(globmod.glob(args.pattern, recursive=True)):
            print(path)
    elif args.cmd == 'exists':
        for path in args.path:
            e = os.path.exists(path)
            kind = 'dir' if os.path.isdir(path) else 'file' if os.path.isfile(path) else 'link' if os.path.islink(path) else '?'
            print(f"{'✓' if e else '✗'} {path}" + (f" ({kind})" if e else ""))
        sys.exit(0 if all(os.path.exists(pa) for pa in args.path) else 1)
    elif args.cmd == 'common':
        print(os.path.commonpath(args.paths))
    elif args.cmd == 'rename':
        import re
        for f in args.files:
            new = re.sub(args.pattern, args.replacement, os.path.basename(f))
            new_path = os.path.join(os.path.dirname(f), new)
            if f != new_path:
                print(f"  {f} → {new_path}")

if __name__ == '__main__':
    main()
