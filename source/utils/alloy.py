"""
    utils/alloy
    ~~~~~~~~~~~

    The Alloy domain.
    Based off sphinx.domains.javascript

    
    :copyright: Alloy Board
    :license: BSD, see LICENSE for details.
"""

"""
    sphinx.domains.javascript
    The JavaScript domain.

    :copyright: Copyright 2007-2019 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType
from sphinx.domains.python import _pseudo_parse_arglist
from sphinx.locale import _
from sphinx.roles import XRefRole
from sphinx.util.docfields import Field, GroupedField, TypedField
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import make_refnode

if False:
    # For type annotation
    from typing import Any, Dict, Iterator, List, Tuple  # NOQA
    from docutils import nodes  # NOQA
    from sphinx.application import Sphinx  # NOQA
    from sphinx.builders import Builder  # NOQA
    from sphinx.environment import BuildEnvironment  # NOQA


class AlloyObject(ObjectDescription):
    """
    Description of a Alloy object.
    """
    #: If set to ``True`` this object is callable and a `desc_parameterlist` is
    #: added
    has_arguments = False

    #: what is displayed right before the documentation entry
    display_prefix = None  # type: str

    #: If ``allow_nesting`` is ``True``, the object prefixes will be accumulated
    #: based on directive nesting
    allow_nesting = False

    def handle_signature(self, sig, signode):
        # type: (str, addnodes.desc_signature) -> Tuple[str, str]
        """Breaks down construct signatures

        Parses out prefix and argument list from construct definition. The
        namespace and class will be determined by the nesting of domain
        directives.
        """
        sig = sig.strip()
        if '(' in sig and sig[-1:] == ')':
            member, arglist = sig.split('(', 1)
            member = member.strip()
            arglist = arglist[:-1].strip()
        else:
            member = sig
            arglist = None
        # If construct is nested, prefix the current prefix
        prefix = self.env.ref_context.get('als:object', None)
        mod_name = self.env.ref_context.get('als:module')
        name = member
        try:
            member_prefix, member_name = member.rsplit('.', 1)

        except ValueError:
            member_name = name
            member_prefix = ''
        finally:
            name = member_name
            if prefix and member_prefix:
                prefix = '.'.join([prefix, member_prefix])
            elif prefix is None and member_prefix:
                prefix = member_prefix
        fullname = name
        if prefix:
            fullname = '.'.join([prefix, name])

        signode['module'] = mod_name
        signode['object'] = prefix
        signode['fullname'] = fullname

        if self.display_prefix:
            signode += addnodes.desc_annotation(self.display_prefix,
                                                self.display_prefix)
        if prefix:
            signode += addnodes.desc_addname(prefix + '.', prefix + '.')
        elif mod_name:
            signode += addnodes.desc_addname(mod_name + '.', mod_name + '.')
        signode += addnodes.desc_name(name, name)
        if self.has_arguments:
            if not arglist:
                signode += addnodes.desc_parameterlist()
            else:
                _pseudo_parse_arglist(signode, arglist)
        return fullname, prefix

    def add_target_and_index(self, name_obj, sig, signode):
        # type: (Tuple[str, str], str, addnodes.desc_signature) -> None
        mod_name = self.env.ref_context.get('als:module')
        fullname = (mod_name and mod_name + '/' or '') + name_obj[0]
        # Alloy predicates use [], not (), so Sphinx includes the arguments in the id
        if "[" in fullname and fullname[0] != "[":
            fullname = fullname.split('[')[0]
        if fullname not in self.state.document.ids:
            signode['names'].append(fullname)
            signode['ids'].append(fullname.replace('$', '_S_'))
            signode['first'] = not self.names
            self.state.document.note_explicit_target(signode)
            objects = self.env.domaindata['als']['objects']
            if fullname in objects:
                self.state_machine.reporter.warning(
                    'duplicate object description of %s, ' % fullname +
                    'other instance in ' +
                    self.env.doc2path(objects[fullname][0]),
                    line=self.lineno)
            objects[fullname] = self.env.docname, self.objtype

        # Todo have this also sweep self.options.get('also', '').split(','):
        indextext = self.get_index_text(mod_name, name_obj)
        if indextext:
            self.indexnode['entries'].append(('single', indextext,
                                              fullname.replace('$', '_S_'),
                                              '', None))

    def get_index_text(self, objectname, name_obj):
        # type: (str, Tuple[str, str]) -> str
        name, obj = name_obj
        name = name.split('[')[0] # Hack to remove the params from fun and pred
        if name == '':
            return ''
        if self.objtype == 'function':
            return _(f"{name} (function)")
        elif self.objtype == 'macro':
            return _('%s (macro)') % (name)
        elif self.objtype == 'predicate':
            return _('%s (predicate)') % (name)
        return ''

    def before_content(self):
        # type: () -> None
        """Handle object nesting before content

        :py:class:`AlloyObject` represents Alloy language constructs. For
        constructs that are nestable, this method will build up a stack of the
        nesting heirarchy so that it can be later de-nested correctly, in
        :py:meth:`after_content`.

        For constructs that aren't nestable, the stack is bypassed, and instead
        only the most recent object is tracked. This object prefix name will be
        removed with :py:meth:`after_content`.

        The following keys are used in ``self.env.ref_context``:

            als:objects
                Stores the object prefix history. With each nested element, we
                add the object prefix to this list. When we exit that object's
                nesting level, :py:meth:`after_content` is triggered and the
                prefix is removed from the end of the list.

            als:object
                Current object prefix. This should generally reflect the last
                element in the prefix history
        """
        prefix = None
        if self.names:
            (obj_name, obj_name_prefix) = self.names.pop()
            prefix = obj_name_prefix.strip('.') if obj_name_prefix else None
            if self.allow_nesting:
                prefix = obj_name
        if prefix:
            self.env.ref_context['als:object'] = prefix
            if self.allow_nesting:
                objects = self.env.ref_context.setdefault('als:objects', [])
                objects.append(prefix)

    def after_content(self):
        # type: () -> None
        """Handle object de-nesting after content

        If this class is a nestable object, removing the last nested class prefix
        ends further nesting in the object.

        If this class is not a nestable object, the list of classes should not
        be altered as we didn't affect the nesting levels in
        :py:meth:`before_content`.
        """
        objects = self.env.ref_context.setdefault('als:objects', [])
        if self.allow_nesting:
            try:
                objects.pop()
            except IndexError:
                pass
        self.env.ref_context['als:object'] = (objects[-1] if len(objects) > 0
                                             else None)


class AlloyCallable(AlloyObject):
    """Description of a Alloy function, macro or predicate."""
    has_arguments = False
    # True makes it tack on (), we use [] instead
    # Means we lose some affordances, but nothing game-changing

    doc_field_types = [
        TypedField('arguments', label=_('Arguments'),
                   names=('argument', 'arg', 'parameter', 'param'),
                   typerolename='func', typenames=('paramtype', 'type')),
        Field('returnvalue', label=_('Returns'), has_arg=False,
              names=('returns', 'return')),
        Field('also', label=_('See Also'), has_arg=False,
              names=('also',)),
        Field('returntype', label=_('Return type'), has_arg=False,
              names=('rtype',)),
    ]

class AlloyMacro(AlloyCallable):
    """Description of an Alloy macro."""
    has_arguments = False
    display_prefix = "let "

    doc_field_types = [
        TypedField('arguments', label=_('Arguments'),
                   names=('argument', 'arg', 'parameter', 'param'),
                   typerolename='func', typenames=('paramtype', 'type')),
        Field('expandsto', label=_('Expands to'), has_arg=False,
              names=('expand', 'expansion')),
    ]

class AlloyFunction(AlloyCallable):
    """Description of an Alloy function."""
    has_arguments = False
    display_prefix = "fun "

class AlloyPredicate(AlloyCallable):
    """Description of an Alloy predicate."""
    has_arguments = False
    display_prefix = "pred "

class AlloyModule(SphinxDirective):
    """
    Directive to mark description of a new Alloy module.

    This directive specifies the module name that will be used by objects that
    follow this directive.

    Options
    -------

    noindex
        If the ``noindex`` option is specified, no linkable elements will be
        created, and the module won't be added to the global module index. This
        is useful for splitting up the module definition across multiple
        sections or files.

    :param mod_name: Module name
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'noindex': directives.flag
    }

    def run(self):
        # type: () -> List[nodes.Node]
        mod_name = self.arguments[0].strip()
        self.env.ref_context['als:module'] = mod_name
        noindex = 'noindex' in self.options
        ret = []  # type: List[nodes.Node]
        if not noindex:
            self.env.domaindata['als']['modules'][mod_name] = self.env.docname
            # Make a duplicate entry in 'objects' to facilitate searching for
            # the module in AlloyDomain.find_obj()
            self.env.domaindata['als']['objects'][mod_name] = (self.env.docname, 'module')
            targetnode = nodes.target('', '', ids=['module-' + mod_name],
                                      ismod=True)
            self.state.document.note_explicit_target(targetnode)
            ret.append(targetnode)
            indextext = _('%s (module)') % mod_name
            inode = addnodes.index(entries=[('single', indextext,
                                             'module-' + mod_name, '', None)])
            ret.append(inode)
        return ret


class AlloyXRefRole(XRefRole):
    def process_link(self, env, refnode, has_explicit_title, title, target):
        # type: (BuildEnvironment, nodes.Element, bool, str, str) -> Tuple[str, str]
        # basically what sphinx.domains.python.PyXRefRole does
        # TODO probably should change this to use Alloy module syntax
        refnode['als:object'] = env.ref_context.get('als:object')
        refnode['als:module'] = env.ref_context.get('als:module')
        if not has_explicit_title:
            title = title.lstrip('.')
            target = target.lstrip('~')
            if title[0:1] == '~':
                title = title[1:]
                dot = title.rfind('.')
                if dot != -1:
                    title = title[dot + 1:]
        return title, target


class AlloyDomain(Domain):
    """Alloy language domain."""
    name = 'als'
    label = 'Alloy'
    
    object_types = {
        'function':  ObjType(_('function'),  'func'),
        'predicate':    ObjType(_('predicate'),    'pred'),
        'macro':     ObjType(_('macro'), 'macro'),
        'module':    ObjType(_('module'),    'mod'),
    }
    directives = {
        'function':  AlloyFunction,
        'predicate':  AlloyPredicate,
        'macro':    AlloyMacro,
        'module':    AlloyModule,
    }
    roles = {
        'func':  AlloyXRefRole(),
        'pred':  AlloyXRefRole(),
        'macro':  AlloyXRefRole(),
        'mod':   AlloyXRefRole(),
    }
    initial_data = {
        'objects': {},  # fullname -> docname, objtype
        'modules': {},  # mod_name -> docname
    }  # type: Dict[str, Dict[str, Tuple[str, str]]]

    def clear_doc(self, docname):
        # type: (str) -> None
        for fullname, (pkg_docname, _l) in list(self.data['objects'].items()):
            if pkg_docname == docname:
                del self.data['objects'][fullname]
        for mod_name, pkg_docname in list(self.data['modules'].items()):
            if pkg_docname == docname:
                del self.data['modules'][mod_name]

    def merge_domaindata(self, docnames, otherdata):
        # type: (List[str], Dict) -> None
        # XXX check duplicates
        for fullname, (fn, objtype) in otherdata['objects'].items():
            if fn in docnames:
                self.data['objects'][fullname] = (fn, objtype)
        for mod_name, pkg_docname in otherdata['modules'].items():
            if pkg_docname in docnames:
                self.data['modules'][mod_name] = pkg_docname

    def find_obj(self, env, mod_name, prefix, name, typ, searchorder=0):
        # type: (BuildEnvironment, str, str, str, str, int) -> Tuple[str, Tuple[str, str]]
        if name[-2:] == '()':
            name = name[:-2]
        objects = self.data['objects']

        searches = []
        if mod_name and prefix:
            searches.append('/'.join([mod_name, prefix, name]))
        if mod_name:
            searches.append('/'.join([mod_name, name]))
        if prefix:
            searches.append('/'.join([prefix, name]))
        searches.append(name)

        if searchorder == 0:
            searches.reverse()

        newname = None
        for search_name in searches:
            if search_name in objects:
                newname = search_name

        return newname, objects.get(newname)

    def resolve_xref(self, env, fromdocname, builder, typ, target, node,
                     contnode):
        # type: (BuildEnvironment, str, Builder, str, str, addnodes.pending_xref, nodes.Element) -> nodes.Element  # NOQA
        mod_name = node.get('als:module')
        prefix = node.get('als:object')
        searchorder = node.hasattr('refspecific') and 1 or 0
        name, obj = self.find_obj(env, mod_name, prefix, target, typ, searchorder)
        if not obj:
            return None
        return make_refnode(builder, fromdocname, obj[0],
                            name.replace('$', '_S_'), contnode, name)

    def resolve_any_xref(self, env, fromdocname, builder, target, node,
                         contnode):
        # type: (BuildEnvironment, str, Builder, str, addnodes.pending_xref, nodes.Element) -> List[Tuple[str, nodes.Element]]  # NOQA
        mod_name = node.get('als:module')
        prefix = node.get('als:object')
        name, obj = self.find_obj(env, mod_name, prefix, target, None, 1)
        if not obj:
            return []
        return [('als:' + self.role_for_objtype(obj[1]),
                 make_refnode(builder, fromdocname, obj[0],
                              name.replace('$', '_S_'), contnode, name))]

    def get_objects(self):
        # type: () -> Iterator[Tuple[str, str, str, str, str, int]]
        for refname, (docname, type) in list(self.data['objects'].items()):
            yield refname, refname, type, docname, \
                refname.replace('$', '_S_'), 1

    def get_full_qualified_name(self, node):
        # type: (nodes.Element) -> str
        modname = node.get('als:module')
        prefix = node.get('als:object')
        target = node.get('reftarget')
        if target is None:
            return None
        else:
            return '/'.join(filter(None, [modname, prefix, target]))


def setup(app):
    # type: (Sphinx) -> Dict[str, Any]
    app.add_domain(AlloyDomain)

    return {
        'env_version': 1,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

