import uuid
from enum import Enum

from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql.operators import and_
from toolz.curried import compose_left, map

from openagent.db.database import DBSession
from openagent.db.models import ChatSession
from openagent.dto.session import (
    SessionTab,
    SessionTreeNodeDTO,
    SessionTreeNodeDTOType,
    build_session_tree_node,
)


def create_session_folder(user_id: str, title: str, parent_folder_id: str | None, order):
    with DBSession() as db_session:
        if parent_folder_id is not None:
            try:
                _ = (
                    db_session.query(ChatSession)
                    .filter(
                        and_(
                            ChatSession.type == SessionTreeNodeDTOType.folder,
                            and_(
                                ChatSession.user_id == user_id,
                                ChatSession.session_id == parent_folder_id,
                            ),
                        )
                    )
                    .one()
                )
            except NoResultFound:
                raise ValueError("Parent folder not found")
        folder = ChatSession(
            user_id=user_id,
            title=title,
            parent_id=parent_folder_id,
            session_id=str(uuid.uuid4()),
            order=order,
            type=SessionTreeNodeDTOType.folder,
            tab=SessionTab.favorite,
        )
        db_session.add(folder)
        db_session.commit()


def update_session(
    user_id: str,
    session_id: str,
    title: str | None,
    order: int | None,
    tab: SessionTab | None,
    parent_id: str | None,
):
    with DBSession() as db_session:
        try:
            session = (
                db_session.query(ChatSession)
                .filter(
                    and_(
                        ChatSession.user_id == user_id,
                        ChatSession.session_id == session_id,
                    )
                )
                .one()
            )
        except NoResultFound:
            raise ValueError("Session not found")
        if title is not None:
            session.title = title
        if order is not None:
            session.order = order
        if tab is not None:
            session.tab = tab
        if parent_id is not None:
            try:
                parent_session = (
                    db_session.query(ChatSession)
                    .filter(
                        and_(
                            ChatSession.user_id == user_id,
                            ChatSession.session_id == parent_id,
                        )
                    )
                    .one()
                )
                if parent_session.type == SessionTreeNodeDTOType.session and session.type == SessionTreeNodeDTOType.folder:
                    raise ValueError("Can't move folder to session")
                if parent_session.parent_id == session_id:
                    raise ValueError("Can't move folder to child")
                if parent_session.deleted_at is not None:
                    raise ValueError("Parent session is deleted")
                if session.deleted_at is not None:
                    raise ValueError("Session is deleted")

            except NoResultFound:
                raise ValueError("Parent session not found")
            session.parent_id = parent_id
        db_session.commit()
        return session


class SessionMoveDirection(str, Enum):
    f2f = "favorite2favorite"
    f2r = "favorite2recent"
    r2f = "recent2favorite"
    r2r = "recent2recent"


def calc_session_move_direction(from_session_tab, to_session_tab):
    recent = SessionTab.recent
    favorite = SessionTab.favorite

    if to_session_tab is recent and from_session_tab is recent:
        return SessionMoveDirection.r2r

    if to_session_tab is favorite and from_session_tab is favorite:
        return SessionMoveDirection.f2f

    if to_session_tab is favorite and from_session_tab is recent:
        return SessionMoveDirection.r2f

    if to_session_tab is recent and from_session_tab is favorite:
        return SessionMoveDirection.f2r


def move_session_folder(
    user_id: str,
    from_session_id: str,
    to_session_id: str | None,
    to_session_tab: SessionTab,
):
    with DBSession() as db_session:
        from_session = fetch_from_session(db_session, from_session_id, user_id)

        from_session_tab = from_session.tab
        direction = calc_session_move_direction(from_session_tab, to_session_tab)

        if direction is SessionMoveDirection.r2r:
            raise ValueError("Can't move recent to recent")

        if direction is SessionMoveDirection.f2r:
            from_session.parent_id = None
            from_session.tab = to_session_tab
            db_session.commit()
            return

        if direction is SessionMoveDirection.f2f or direction is SessionMoveDirection.r2f:
            if to_session_id is None:
                from_session.parent_id = None
                from_session.tab = to_session_tab
                db_session.commit()
                return

            parent_session = fetch_parent_session(db_session, to_session_id, user_id)

            if parent_session.type == SessionTreeNodeDTOType.session:
                raise ValueError("Can't move folder to session")
            if parent_session.parent_id == from_session_id:
                raise ValueError("Can't move folder to child")

            from_session.parent_id = to_session_id
            db_session.commit()


def fetch_parent_session(db_session, to_session_id, user_id):
    try:
        parent_session = (
            db_session.query(ChatSession)
            .filter(
                and_(
                    ChatSession.user_id == user_id,
                    ChatSession.session_id == to_session_id,
                )
            )
            .one()
        )

    except NoResultFound:
        raise ValueError("Parent session not found")
    return parent_session


def fetch_from_session(db_session, from_session_id, user_id):
    try:
        session = (
            db_session.query(ChatSession)
            .filter(
                and_(
                    ChatSession.user_id == user_id,
                    ChatSession.session_id == from_session_id,
                )
            )
            .one()
        )
    except NoResultFound:
        raise ValueError("Session not found")
    return session


def build_folder_tree(
    nodes: list[SessionTreeNodeDTO],
    parent_id: int | None = None,
):
    unsorted_tree = do_build_folder_tree(nodes, parent_id)
    return sorted(unsorted_tree)


def do_build_folder_tree(nodes, parent_id):
    tree = []
    for node in nodes:
        if node.parent_id == parent_id:
            session_nodes = do_build_folder_tree(nodes, node.session_id)
            node.children = build_sorted_children(node.children, session_nodes)
            tree.append(node)
    return tree


def build_sorted_children(old_children: list[SessionTreeNodeDTO], new_children: list[SessionTreeNodeDTO]):
    old_children = old_children or []
    new_children = new_children or []
    unique_children = list(set(old_children + new_children))
    sorted_children = sorted(unique_children, key=lambda x: (x.order, x.created_at), reverse=True)
    return sorted_children


def get_session_tree(user_id: str) -> list[SessionTreeNodeDTO]:
    with DBSession() as db_session:
        sessions = db_session.query(ChatSession).filter_by(user_id=user_id, deleted_at=None, tab=SessionTab.favorite).all()
        session_tree_nodes: list[SessionTreeNodeDTO] = compose_left(map(build_session_tree_node), list)(sessions)

        tree = build_folder_tree(session_tree_nodes)
        return tree
