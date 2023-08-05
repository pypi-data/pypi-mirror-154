
# Autogenerated by mlir-tblgen; don't manually edit.

from ._ods_common import _cext as _ods_cext
from ._ods_common import extend_opview_class as _ods_extend_opview_class, segmented_accessor as _ods_segmented_accessor, equally_sized_accessor as _ods_equally_sized_accessor, get_default_loc_context as _ods_get_default_loc_context, get_op_result_or_value as _get_op_result_or_value, get_op_results_or_values as _get_op_results_or_values
_ods_ir = _ods_cext.ir

try:
  from . import _msft_ops_ext as _ods_ext_module
except ImportError:
  _ods_ext_module = None

import builtins


@_ods_cext.register_dialect
class _Dialect(_ods_ir.Dialect):
  DIALECT_NAMESPACE = "msft"
  pass


@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ChannelOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.constructs.channel"

  _ODS_REGIONS = (0, True)

  def __init__(self, input, clk, sym_name, defaultStages, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(input))
    operands.append(_get_op_result_or_value(clk))
    attributes["sym_name"] = sym_name
    attributes["defaultStages"] = defaultStages
    _ods_context = _ods_get_default_loc_context(loc)
    results = _ods_ir.InferTypeOpInterface(ChannelOp).inferReturnTypes(
        operands=operands,
        attributes=_ods_ir.DictAttr.get(attributes, context=_ods_context),
        context=_ods_context,
        loc=loc)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def input(self):
    return self.operation.operands[0]

  @builtins.property
  def clk(self):
    return self.operation.operands[1]

  @builtins.property
  def sym_name(self):
    return _ods_ir.StringAttr(self.operation.attributes["sym_name"])

  @sym_name.setter
  def sym_name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["sym_name"] = value

  @builtins.property
  def defaultStages(self):
    return _ods_ir.IntegerAttr(self.operation.attributes["defaultStages"])

  @defaultStages.setter
  def defaultStages(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["defaultStages"] = value

  @builtins.property
  def output(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class DeclPhysicalRegionOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.physical_region"

  _ODS_REGIONS = (0, True)

  def __init__(self, sym_name, bounds, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    attributes["sym_name"] = sym_name
    attributes["bounds"] = bounds
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def sym_name(self):
    return _ods_ir.StringAttr(self.operation.attributes["sym_name"])

  @sym_name.setter
  def sym_name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["sym_name"] = value

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class DesignPartitionOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.partition"

  _ODS_REGIONS = (0, True)

  def __init__(self, sym_name, verilogName, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    attributes["sym_name"] = sym_name
    attributes["verilogName"] = verilogName
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def sym_name(self):
    return _ods_ir.StringAttr(self.operation.attributes["sym_name"])

  @sym_name.setter
  def sym_name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["sym_name"] = value

  @builtins.property
  def verilogName(self):
    return _ods_ir.StringAttr(self.operation.attributes["verilogName"])

  @verilogName.setter
  def verilogName(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["verilogName"] = value

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class DynamicInstanceOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.instance.dynamic"

  _ODS_REGIONS = (1, True)

  def __init__(self, instanceRef, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    attributes["instanceRef"] = instanceRef
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def body(self):
    return self.regions[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class DynamicInstanceVerbatimAttrOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.instance.verb_attr"

  _ODS_REGIONS = (0, True)

  def __init__(self, name, value, *, subPath=None, ref=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    attributes["name"] = name
    attributes["value"] = value
    if subPath is not None: attributes["subPath"] = subPath
    if ref is not None: attributes["ref"] = ref
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def name(self):
    return _ods_ir.StringAttr(self.operation.attributes["name"])

  @name.setter
  def name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["name"] = value

  @builtins.property
  def value(self):
    return _ods_ir.StringAttr(self.operation.attributes["value"])

  @value.setter
  def value(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["value"] = value

  @builtins.property
  def subPath(self):
    if "subPath" not in self.operation.attributes:
      return None
    return _ods_ir.StringAttr(self.operation.attributes["subPath"])

  @subPath.setter
  def subPath(self, value):
    if value is not None:
      self.operation.attributes["subPath"] = value
    elif "subPath" in self.operation.attributes:
      del self.operation.attributes["subPath"]

  @subPath.deleter
  def subPath(self):
    del self.operation.attributes["subPath"]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class EntityExternOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.entity.extern"

  _ODS_REGIONS = (0, True)

  def __init__(self, sym_name, metadata, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    attributes["sym_name"] = sym_name
    attributes["metadata"] = metadata
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def sym_name(self):
    return _ods_ir.StringAttr(self.operation.attributes["sym_name"])

  @sym_name.setter
  def sym_name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["sym_name"] = value

  @builtins.property
  def metadata(self):
    return _ods_ir.Attribute(self.operation.attributes["metadata"])

  @metadata.setter
  def metadata(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["metadata"] = value

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class InstanceHierarchyOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.instance.hierarchy"

  _ODS_REGIONS = (1, True)

  def __init__(self, topModuleRef, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    attributes["topModuleRef"] = topModuleRef
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def body(self):
    return self.regions[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class InstanceOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.instance"

  _ODS_REGIONS = (0, True)

  def __init__(self, result, sym_name, moduleName, inputs, *, parameters=None, targetDesignPartition=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.extend(_get_op_results_or_values(inputs))
    attributes["sym_name"] = sym_name
    attributes["moduleName"] = moduleName
    if parameters is not None: attributes["parameters"] = parameters
    if targetDesignPartition is not None: attributes["targetDesignPartition"] = targetDesignPartition
    results.extend(result)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def inputs(self):
    _ods_variadic_group_length = len(self.operation.operands) - 1 + 1
    return self.operation.operands[0:0 + _ods_variadic_group_length]

  @builtins.property
  def sym_name(self):
    return _ods_ir.StringAttr(self.operation.attributes["sym_name"])

  @sym_name.setter
  def sym_name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["sym_name"] = value

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class MSFTModuleExternOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.module.extern"

  _ODS_REGIONS = (1, True)

  @builtins.property
  def verilogName(self):
    if "verilogName" not in self.operation.attributes:
      return None
    return _ods_ir.StringAttr(self.operation.attributes["verilogName"])

  @verilogName.setter
  def verilogName(self, value):
    if value is not None:
      self.operation.attributes["verilogName"] = value
    elif "verilogName" in self.operation.attributes:
      del self.operation.attributes["verilogName"]

  @verilogName.deleter
  def verilogName(self):
    del self.operation.attributes["verilogName"]

  @builtins.property
  def body(self):
    return self.regions[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class MSFTModuleOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.module"

  _ODS_REGIONS = (1, True)

  @builtins.property
  def fileName(self):
    if "fileName" not in self.operation.attributes:
      return None
    return _ods_ir.StringAttr(self.operation.attributes["fileName"])

  @fileName.setter
  def fileName(self, value):
    if value is not None:
      self.operation.attributes["fileName"] = value
    elif "fileName" in self.operation.attributes:
      del self.operation.attributes["fileName"]

  @fileName.deleter
  def fileName(self):
    del self.operation.attributes["fileName"]

  @builtins.property
  def body(self):
    return self.regions[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class OutputOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.output"

  _ODS_REGIONS = (0, True)

  def __init__(self, operands_, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.extend(_get_op_results_or_values(operands_))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def operands_(self):
    _ods_variadic_group_length = len(self.operation.operands) - 1 + 1
    return self.operation.operands[0:0 + _ods_variadic_group_length]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class PDPhysLocationOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.pd.location"

  _ODS_REGIONS = (0, True)

  def __init__(self, loc_, *, subPath=None, ref=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    attributes["loc"] = loc_
    if subPath is not None: attributes["subPath"] = subPath
    if ref is not None: attributes["ref"] = ref
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def subPath(self):
    if "subPath" not in self.operation.attributes:
      return None
    return _ods_ir.StringAttr(self.operation.attributes["subPath"])

  @subPath.setter
  def subPath(self, value):
    if value is not None:
      self.operation.attributes["subPath"] = value
    elif "subPath" in self.operation.attributes:
      del self.operation.attributes["subPath"]

  @subPath.deleter
  def subPath(self):
    del self.operation.attributes["subPath"]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class PDPhysRegionOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.pd.physregion"

  _ODS_REGIONS = (0, True)

  def __init__(self, physRegionRef, *, subPath=None, ref=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    attributes["physRegionRef"] = physRegionRef
    if subPath is not None: attributes["subPath"] = subPath
    if ref is not None: attributes["ref"] = ref
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def subPath(self):
    if "subPath" not in self.operation.attributes:
      return None
    return _ods_ir.StringAttr(self.operation.attributes["subPath"])

  @subPath.setter
  def subPath(self, value):
    if value is not None:
      self.operation.attributes["subPath"] = value
    elif "subPath" in self.operation.attributes:
      del self.operation.attributes["subPath"]

  @subPath.deleter
  def subPath(self):
    del self.operation.attributes["subPath"]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class PDRegPhysLocationOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.pd.reg_location"

  _ODS_REGIONS = (0, True)

  def __init__(self, locs, *, ref=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    attributes["locs"] = locs
    if ref is not None: attributes["ref"] = ref
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class PEOutputOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.pe.output"

  _ODS_REGIONS = (0, True)

  def __init__(self, output, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(output))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def output(self):
    return self.operation.operands[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class SystolicArrayOp(_ods_ir.OpView):
  OPERATION_NAME = "msft.systolic.array"

  _ODS_REGIONS = (1, True)

  def __init__(self, peOutputs, rowInputs, colInputs, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(rowInputs))
    operands.append(_get_op_result_or_value(colInputs))
    results.append(peOutputs)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def rowInputs(self):
    return self.operation.operands[0]

  @builtins.property
  def colInputs(self):
    return self.operation.operands[1]

  @builtins.property
  def peOutputs(self):
    return self.operation.results[0]

  @builtins.property
  def pe(self):
    return self.regions[0]
