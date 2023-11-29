from server.db.models.knowledge_base_model import KnowledgeBaseModel
from server.db.session import with_session


@with_session
def add_kb_to_db(session, kb_name, kb_info, vs_type, embed_model):
    if (
        kb := session.query(KnowledgeBaseModel)
        .filter_by(kb_name=kb_name)
        .first()
    ):
        kb.kb_info = kb_info
        kb.vs_type = vs_type
        kb.embed_model = embed_model
    else:
        kb = KnowledgeBaseModel(kb_name=kb_name, kb_info=kb_info, vs_type=vs_type, embed_model=embed_model)
        session.add(kb)
    return True


@with_session
def list_kbs_from_db(session, min_file_count: int = -1):
    kbs = session.query(KnowledgeBaseModel.kb_name).filter(KnowledgeBaseModel.file_count > min_file_count).all()
    kbs = [kb[0] for kb in kbs]
    return kbs


@with_session
def kb_exists(session, kb_name):
    kb = session.query(KnowledgeBaseModel).filter_by(kb_name=kb_name).first()
    return bool(kb)


@with_session
def load_kb_from_db(session, kb_name):
    if (
        kb := session.query(KnowledgeBaseModel)
        .filter_by(kb_name=kb_name)
        .first()
    ):
        kb_name, vs_type, embed_model = kb.kb_name, kb.vs_type, kb.embed_model
    else:
        kb_name, vs_type, embed_model = None, None, None
    return kb_name, vs_type, embed_model


@with_session
def delete_kb_from_db(session, kb_name):
    if (
        kb := session.query(KnowledgeBaseModel)
        .filter_by(kb_name=kb_name)
        .first()
    ):
        session.delete(kb)
    return True


@with_session
def get_kb_detail(session, kb_name: str) -> dict:
    if (
        kb := session.query(KnowledgeBaseModel)
        .filter_by(kb_name=kb_name)
        .first()
    ):
        return {
            "kb_name": kb.kb_name,
            "kb_info": kb.kb_info,
            "vs_type": kb.vs_type,
            "embed_model": kb.embed_model,
            "file_count": kb.file_count,
            "create_time": kb.create_time,
        }
    else:
        return {}
