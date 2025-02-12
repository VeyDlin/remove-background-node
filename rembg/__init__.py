
from __future__ import annotations

from typing import List

from .base import BaseSession
from .bg import remove

sessions_class: List[type[BaseSession]] = []

from .birefnet_general import BiRefNetSessionGeneral
sessions_class.append(BiRefNetSessionGeneral)

from .birefnet_general_lite import BiRefNetSessionGeneralLite
sessions_class.append(BiRefNetSessionGeneralLite)

from .birefnet_portrait import BiRefNetSessionPortrait
sessions_class.append(BiRefNetSessionPortrait)

from .birefnet_dis import BiRefNetSessionDIS
sessions_class.append(BiRefNetSessionDIS)

from .birefnet_hrsod import BiRefNetSessionHRSOD
sessions_class.append(BiRefNetSessionHRSOD)

from .birefnet_cod import BiRefNetSessionCOD
sessions_class.append(BiRefNetSessionCOD)

from .birefnet_massive import BiRefNetSessionMassive
sessions_class.append(BiRefNetSessionMassive)

from .dis_anime import DisSession
sessions_class.append(DisSession)

from .dis_general_use import DisSession as DisSessionGeneralUse
sessions_class.append(DisSessionGeneralUse)

from .silueta import SiluetaSession
sessions_class.append(SiluetaSession)

from .u2net_cloth_seg import Unet2ClothSession
sessions_class.append(Unet2ClothSession)

from .u2net_human_seg import U2netHumanSegSession
sessions_class.append(U2netHumanSegSession)

from .u2net import U2netSession
sessions_class.append(U2netSession)

from .u2netp import U2netpSession
sessions_class.append(U2netpSession)

from .bria_rmbg import BriaRmBgSession
sessions_class.append(BriaRmBgSession)
